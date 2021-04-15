import argparse
from utils import sys_utils
from utils import video_utils

def extract_dataset_frames(dataset_name, dataset_dir, output_dir, resizing_dims = (-1,-1), sample_rate='fixed-16'):
	'''
	Given a list of video paths extracts their frames into corresponding folders under the output_dir
	Input:
		dataset_dir: string; the path to dataset contaitning 'videos'. ex. '/path_to_dataset/dataset'
		output_dir: string; the target path for frame extraction. ex. '/path_to_dataset/frames'
		resizing_dims: resizing frames.
				   	 resize the smaller dim target_dim[0]; and 
				   	 resize the larger dim to target_dim[1]; and
				   	 if target_dim[0] or target_dim[1] is set to -1, the dims change while preserving the aspect ratio;
				   	 if target_dim = (-1,-1) there is no resizing. the original sims are maintained. 
	Output:
		int: number of videos for which it extracted the frames
	'''

	# extract Tempuckey frames
	if dataset_name == 'Tempuckey': 
		sys_utils.create_folder(output_dir)

		# list of filepath
		video_paths = sys_utils.get_files_path('{}/videos'.format(dataset_dir))
		empty_videos = []
		for vpath in video_paths:
			video_name = vpath.split('/')[-1]
			fdir = '{}/{}'.format(output_dir, video_name)
			print('extracting frames to', fdir)
			sys_utils.create_folder(fdir)
			sr = sample_rate.split('-')
			if len(sr)!=2:
				print('invalid sample rate!\n ex. fixed-xx, fps-xx, fixed-16, fps-30')
				return -1
			sample_method,sample_cnt = sr[0],int(sr[1])
			if sample_method=='fixed':
				try:
					fps, duration, num_frames = video_utils.get_video_information(vpath)
					fps = float(sample_cnt)/duration
				except Exception as e:
					print(vpath, e)
					empty_videos.append(vpath)
				count = video_utils.get_video_frames(vpath, fdir, fps = fps, resizing_dims = resizing_dims)
			elif sample_method=='fps':
				fps = sample_cnt
				count = video_utils.get_video_frames(vpath, fdir, fps = fps, resizing_dims = resizing_dims)
			else:
				print('invalid sampling method!')
				return -1
			print('completed extracting {} frames'.format(count))
            
		return len(video_paths)

	# extract UCF101 frames
	elif dataset_name == 'UCF101':
		sys_utils.create_folder(output_dir)

		# list of filepath
		category_paths = sys_utils.get_subfolders_path('{}/videos'.format(dataset_dir))
		category_names = [d.split('/')[-1] for d in category_paths]
		for n in category_names:
			sys_utils.create_folder('{}/{}'.format(output_dir, n))

		video_paths = [sys_utils.get_files_path(p) for p in [d for d in category_paths]]
		video_paths = [p for sublist in video_paths for p in sublist]
		
		for vpath in video_paths:
			video_name = vpath.split('/')[-1].split('.')[-2]
			categ_name = vpath.split('/')[-2]
			fdir = '{}/{}/{}'.format(output_dir, categ_name, video_name)
			if not sys_utils.path_exists(fdir):
				sys_utils.create_folder(fdir)
				print('created {}'.format(fdir))

			print('extracting frames to', fdir)
			count = video_utils.get_video_frames(vpath, fdir, fps = 30, resizing_dims = resizing_dims)
			print('completed extracting {} frames'.format(count))
	else:
		print('frame extraction for your specified dataset name, {}, is not defined!'.format(dataset))

if __name__ == '__main__':

	parser = argparse.ArgumentParser ()
	parser.add_argument('--dataset_name', dest = 'dataset_name', default = 'Tempuckey', help = 'provide the dataset name. ex. Tempuckey; UFC101')
	parser.add_argument('--dataset_dir',  dest = 'dataset_dir',  default = '/path/to/dataset', help = 'provide the path to dataset directory that contains the videos folder')
	parser.add_argument('--output_dir',   dest = 'output_dir',   default = '/path/to/dataset/frames', help = 'provide output directory where the frames should be stored at')

	args = parser.parse_args()

	## python3 extract_dataset_frames.py --dataset_name 'Tempuckey' --dataset_dir '/home/pishu/Desktop/repos/datasets/Tempuckey' --output_dir '/home/pishu/Desktop/repos/datasets/Tempuckey/frames'
	extract_dataset_frames(dataset_name = args.dataset_name,
							 dataset_dir = args.dataset_dir, 
							 output_dir = args.output_dir,
							 resizing_dims = (-1,-1),
							 sample_rate = 'fixed-16')

	## python3 extract_dataset_frames.py --dataset_name 'UCF101' --dataset_dir '/home/pishu/Desktop/repos/datasets/UCF101' --output_dir '/home/pishu/Desktop/repos/datasets/UCF101/frames'
# 	extract_dataset_frames(dataset_name = args.dataset_name,
# 						  dataset_dir = args.dataset_dir,
# 						  output_dir = args.output_dir,
# 						  resizing_dims = (-1,-1))

