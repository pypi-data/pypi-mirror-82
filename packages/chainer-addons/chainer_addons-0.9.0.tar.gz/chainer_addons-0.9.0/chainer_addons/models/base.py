import chainer
import chainer.functions as F

from chainer.serializers import npz
from chainer_addons.links import PoolingType

from collections import OrderedDict
from chainer.initializers import HeNormal

import numpy as np
from abc import ABC, abstractmethod, abstractproperty


class PretrainedModelMixin(ABC):
	CHAINER_PRETRAINED = (
		chainer.links.model.vision.resnet.ResNetLayers,
		chainer.links.model.vision.vgg.VGG16Layers,
		chainer.links.model.vision.googlenet.GoogLeNet,
	)

	def loss(self, pred, gt, loss_func=F.softmax_cross_entropy):
		return loss_func(pred, gt)

	def accuracy(self, pred, gt):
		return F.accuracy(pred, gt)

	def __init__(self, n_classes=1000,
		pooling=PoolingType.Default, pooling_params={}, *args, **kwargs):
		if isinstance(self, PretrainedModelMixin.CHAINER_PRETRAINED):
			super(PretrainedModelMixin, self).__init__(
				pretrained_model=None, *args, **kwargs)
		else:
			super(PretrainedModelMixin, self).__init__(*args, **kwargs)

		if "input_dim" not in pooling_params:
			pooling_params["input_dim"] = self.meta.feature_size

		with self.init_scope():
			self.init_layers(n_classes)
			self.pool = PoolingType.new(pooling, **pooling_params)


	def load_for_finetune(self, weights, n_classes, *, path="", strict=False, headless=False, **kwargs):
		"""
			The weights should be pre-trained on a bigger
			dataset (eg. ImageNet). The classification layer is
			reinitialized after all other weights are loaded
		"""
		self.load(weights, path=path, strict=strict, headless=headless)
		self.reinitialize_clf(n_classes, **kwargs)

	def load_for_inference(self, weights, n_classes, *, path="", strict=False, headless=False, **kwargs):
		"""
			In this use case we are loading already fine-tuned
			weights. This means, we need to reinitialize the
			classification layer first and then load the weights.
		"""
		self.reinitialize_clf(n_classes, **kwargs)
		self.load(weights, path=path, strict=strict, headless=headless)

	def load(self, weights, *, path="", strict=False, headless=False):
		if weights not in [None, "auto"]:
			ignore_names = None
			if headless:
				ignore_names = lambda name: name.startswith(self.clf_layer_name)

			npz.load_npz(weights, self, path=path, strict=strict, ignore_names=ignore_names)


	@property
	def clf_layer_name(self):
		return self.meta.classifier_layers[-1]

	@property
	def clf_layer(self):
		return getattr(self, self.clf_layer_name)

	@classmethod
	def prepare(cls, img, size=None):
		size = size or cls.meta.input_size
		if isinstance(size, int):
			size = (size, size)
		return cls.meta.prepare_func(img, size=size)

	@classmethod
	def prepare_back(cls, img):
		img = img.transpose(1,2,0).copy()
		mean = cls.meta.mean
		if isinstance(mean, np.ndarray):
			mean = mean.squeeze()
		img += mean
		img = img[..., ::-1].astype(np.uint8)
		return img

	def reinitialize_clf(self, n_classes,
		feat_size=None, initializer=None):
		if initializer is None or not callable(initializer):
			initializer = HeNormal(scale=1.0)

		clf_layer = self.clf_layer

		w_shape = (n_classes, feat_size or clf_layer.W.shape[1])
		clf_layer.W.data = np.zeros(w_shape, dtype=np.float32)
		clf_layer.b.data = np.zeros(w_shape[0], dtype=np.float32)
		initializer(clf_layer.W.data)

	@property
	def functions(self):
		return OrderedDict(self._links)

	@abstractmethod
	def init_layers(self, n_classes):
		raise NotImplementedError()

	@abstractproperty
	def _links(self):
		raise NotImplementedError()

	def __call__(self, X, layer_name=None):
		layer_name = layer_name or self.meta.classifier_layers[-1]
		caller = super(PretrainedModelMixin, self).__call__
		activations = caller(X, layers=[layer_name])
		if isinstance(activations, dict):
			activations = activations[layer_name]
		return activations

class BaseClassifier(ABC, chainer.Chain):
	def __init__(self, model, layer_name=None, loss_func=F.softmax_cross_entropy):
		super(BaseClassifier, self).__init__()
		self.layer_name = layer_name or model.meta.classifier_layers[-1]
		self._loss_func = loss_func

		with self.init_scope():
			self.model = model

	def loss(self, pred, y):
		return self.model.loss(pred, y,
			loss_func=self._loss_func)

	def report(self, **values):
		chainer.report(values, self)
