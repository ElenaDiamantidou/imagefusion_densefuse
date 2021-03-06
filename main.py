# Demo - train the DenseFuse network & use it to generate an image

from __future__ import print_function

import time

from train_recons import train_recons
from generate import generate
from utils import list_images
import os

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# IS_TRAINING = True
IS_TRAINING = False
IS_VIDEO = True

BATCH_SIZE = 2
EPOCHES = 4

SSIM_WEIGHTS = [1, 10, 100, 1000]
MODEL_SAVE_PATHS = [
    'D:/project/GitHub/ImageFusion/imagefusion_deep_dense_block/models/deepfuse_dense_model_bs2_epoch4_all_weight_1e0.ckpt',
    'D:/project/GitHub/ImageFusion/imagefusion_deep_dense_block/models/deepfuse_dense_model_bs2_epoch4_all_weight_1e1.ckpt',
    'D:/project/GitHub/ImageFusion/imagefusion_deep_dense_block/models/deepfuse_dense_model_bs2_epoch4_all_weight_1e2.ckpt',
    'D:/project/GitHub/ImageFusion/imagefusion_deep_dense_block/models/deepfuse_dense_model_bs2_epoch4_all_weight_1e3.ckpt',
]

# MODEL_SAVE_PATH = './models/deepfuse_dense_model_bs4_epoch2_relu_pLoss_noconv_test.ckpt'
# model_pre_path  = './models/deepfuse_dense_model_bs2_epoch2_relu_pLoss_noconv_NEW.ckpt'

# In testing process, 'model_pre_path' is set to None
model_pre_path  = None

def main():

	if IS_TRAINING:

		original_imgs_path = list_images('D:/ImageDatabase/Image_fusion_MSCOCO/original/')

		for ssim_weight, model_save_path in zip(SSIM_WEIGHTS, MODEL_SAVE_PATHS):
			print('\nBegin to train the network ...\n')
			train_recons(original_imgs_path, model_save_path, model_pre_path, ssim_weight, EPOCHES, BATCH_SIZE, debug=True)

			print('\nSuccessfully! Done training...\n')
	else:
		if IS_VIDEO:
			ssim_weight = SSIM_WEIGHTS[0]
			model_path = MODEL_SAVE_PATHS[0]

			IR_path = list_images('video/1_IR/')
			VIS_path = list_images('video/1_VIS/')
			output_save_path = 'video/fused'+ str(ssim_weight) +'/'
			generate(IR_path, VIS_path, model_path, model_pre_path,
			         ssim_weight, 0, IS_VIDEO, 'addition', output_path=output_save_path)
		else:
			print('\nBegin to generate pictures ...\n')

			path = 'images/IV_images/'
			for i in range(20):
				index = i + 1
				infrared = path + 'IR' + str(index) + '.png'
				visible = path + 'VIS' + str(index) + '.png'
				fusion_type = 'addition'
				# fusion_type = 'l1'
				for ssim_weight, model_path in zip(SSIM_WEIGHTS, MODEL_SAVE_PATHS):
					output_save_path = 'outputs/fused_deepdense_bs2_epoch4_all_l1_focus_'+str(ssim_weight)

					generate(infrared, visible, model_path, model_pre_path,
					         ssim_weight, index, IS_VIDEO, type = fusion_type, output_path = output_save_path)


if __name__ == '__main__':
    main()

