import argparse
from utils import sys_utils
from utils import video_utils

def write_as_csv(filename, rows):
	with open(filename, 'w') as f:
		for row in rows:
			f.write(row)
	print('generated {}'.format(filename))

def generate_dataset_info_csv(dataset_name, dataset_dir, splits_dir, output_dir):
	'''
	Given the path to the dataset and its extracted frames, generates csv files for train and test splits
	Input:
		dataset_name: str name of the dataset
		dataset_dir: str path to dataset contaitning 'frames'. ex. '/path_to_dataset/frames'
		splits_dir: str path to train/test/val dataset splits
		output_dir: str path to location where the csv files will be stored at 
	Output:
		list of str: paths of generated csv files 
	'''

	output_files = []
	# generate Tempuckey dataset info csv
	if dataset_name == 'Tempuckey': 
		raise NotImplementedError()

	# generate UCF101 dataset info csv
	elif dataset_name == 'UCF101':
		for split in ['train', 'test']:
			for subsplit in ['01','02','03']: # UFC101 has three splits for each train/test split
				fname = '{}/{}list{}.txt'.format(splits_dir, split, subsplit)
				
				output_rows = []
				with open(fname, 'r') as f:
					print('generating {}list{}.csv in progress...'.format(split,subsplit))
					for row in f:
						vidname = row.split('.')[0]
						try:
							video_path = '{}/frames/{}'.format(dataset_dir, vidname)
							frames = sys_utils.get_files_path(video_path)
							if len(frames) != 0:
								line = '{},{}\n'.format(video_path, len(frames))
								output_rows.append(line)
						except FileNotFoundError as e:
							# not all videos have been extracted into frames. skipping file not found.
							pass

				fname = '{}/{}list{}.csv'.format(output_dir, split, subsplit)
				write_as_csv(fname, output_rows)
				output_files.append(fname)
	else:
		print('The specified dataset name, {}, is not defined!'.format(dataset))

	return output_files

if __name__ == '__main__':

	parser = argparse.ArgumentParser ()
	parser.add_argument('--dataset_name', dest = 'dataset_name', default = 'Tempuckey', help = 'provide the dataset name. ex. Tempuckey; UFC101')
	parser.add_argument('--dataset_dir',  dest = 'dataset_dir',  default = '/home/pishu/Desktop/repos/datasets/Tempuckey', help = 'provide the path to dataset directory that contains the videos folder')
	parser.add_argument('--splits_dir',   dest = 'splits_dir',   default = '/home/pishu/Desktop/repos/datasets/Tempuckey/splits', help = 'provide output directory where the frames should be stored at')
	parser.add_argument('--output_dir',   dest = 'output_dir',   default = '/home/pishu/Desktop/repos/datasets/Tempuckey/splits', help = 'provide output directory where the frames should be stored at')

	args = parser.parse_args()

	## python3 generate_dataset_info_csv.py --dataset_name 'Tempuckey' --dataset_dir '/home/pishu/Desktop/repos/datasets/Tempuckey' --splits_dir '/home/pishu/Desktop/repos/datasets/Tempuckey/splits'
	# csv_files = generate_dataset_info_csv(dataset_name = args.dataset_name,	#'Tempuckey',
	# 						 dataset_dir = args.dataset_dir, 	#'/home/pishu/Desktop/repos/datasets/Tempuckey',
	# 						 splits_dir = args.splits_dir,		#'/home/pishu/Desktop/repos/datasets/Tempuckey/splits',
	# 						 output_dir = args.output_dir)		#'/home/pishu/Desktop/repos/datasets/Tempuckey/splits/csv',
	
	# python3 generate_dataset_info_csv.py --dataset_name 'UCF101' --dataset_dir '/home/pishu/Desktop/repos/datasets/UCF101' --splits_dir '/home/pishu/Desktop/repos/datasets/UCF101/splits_classification' --output_dir '/home/pishu/Desktop/repos/datasets/UCF101/splits_classification/csv'
	csv_files = generate_dataset_info_csv(dataset_name = args.dataset_name,	# 'UCF101',
						  dataset_dir = args.dataset_dir, 		# '/home/pishu/Desktop/repos/datasets/UCF101',
						  splits_dir = args.splits_dir,			# '/home/pishu/Desktop/repos/datasets/UCF101/splits_classification'
						  output_dir = args.output_dir)			# '/home/pishu/Desktop/repos/datasets/UCF101/splits_classification/csv'
