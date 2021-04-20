import argparse
import numpy as np
import torch 
import torchvision.models as models
from PIL import Image
from torchvision import transforms
from utils import sys_utils
from utils import video_utils

def get_model(model_name):
    model = getattr(models, model_name)(pretrained=True)
    model.eval()
    return model

def get_feat_vector(path_img, model, layer_name='avgpool'):
    '''
    Input: 
        path_img: string, /path/to/image
        model: a pretrained torch model
        layer name: string, layer name to obtain the features from
    Output:
        my_output: torch.tensor, output of layer_name
    '''
    input_image = Image.open(path_img)
    
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        my_output = None
        
        def my_hook(module_, input_, output_):
            nonlocal my_output
            my_output = output_

        if layer_name == 'avgpool':
            a_hook = model.avgpool.register_forward_hook(my_hook)        
        else:
            raise ValueError('invalid layer name!')
            
        model(input_batch)
        a_hook.remove()
        
        return my_output.reshape(-1)



def extract_dataset_feats(dataset_frames_dir, output_dir, model_name='resnet18'):
    '''
    Given a list of video paths extracts their frames into corresponding folders under the output_dir
    Input:
        input_frames_dir: string; the path to frames. ex. '/path_to_dataset/dataset/frames'
        output_dir: string; the target path for feat extraction. ex. '/path_to_dataset/dataset/feats'
        resizing_dims: resizing frames.
                     resize the smaller dim target_dim[0]; and 
                     resize the larger dim to target_dim[1]; and
                     if target_dim[0] or target_dim[1] is set to -1, the dims change while preserving the aspect ratio;
                     if target_dim = (-1,-1) there is no resizing. the original sims are maintained. 
    Output:
        int: number of videos for which it extracted the frame features
    '''
    sys_utils.create_folder(output_dir)

    model = get_model(model_name=model_name)
    
    # list of frame folders
    frames_dir = sys_utils.get_subfolders_path(dataset_frames_dir)
    for f_dir in frames_dir:
        frames_path = sorted(sys_utils.get_files_path(f_dir))
        
        # create a folder for feats of each video
        if len(frames_path)!=0:
            a_frame_path = frames_path[0]
            video_name = a_frame_path.split('/')[-2]
            fdir = f'{output_dir}/{video_name}'
            sys_utils.create_folder(fdir)
            print('extracting features to', fdir)

        for f_path in frames_path:
            feat = get_feat_vector(f_path, model).cpu().numpy()
            frame_id = f_path.split('/')[-1].split('.')[-2]
            fname = f'{fdir}/{frame_id}.npy'
            np.save(fname, feat)
            
    return len(frames_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser ()
    parser.add_argument('--dataset_frames_dir',  dest = 'dataset_frames_dir',  default = '/path/to/dataset/frames', help = 'provide the path to dataset directory that contains frames for each the videos (separate folder for each video)')
    parser.add_argument('--output_dir',   dest = 'output_dir',   default = '/path/to/dataset/feats/resnet18', help = 'provide output directory where the frame features should be stored at')
    parser.add_argument('--model_name',   dest = 'model_name',   default = 'resnet18', help = 'provide pretrained model name')

    args = parser.parse_args()

    ## python3 extract_dataset_feats.py --dataset_frames_dir '/usr/local/data02/zahra/datasets/Tempuckey/sentence_segments/frames' --output_dir '/usr/local/data02/zahra/datasets/Tempuckey/sentence_segments/feats/resent18' --model_name resnet18
    extract_dataset_feats(dataset_frames_dir = args.dataset_frames_dir,
                             output_dir = args.output_dir,
                             model_name = args.model_name)
    

