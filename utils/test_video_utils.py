import unittest
from utils import video_utils as vu 

class test_video_utils(unittest.TestCase):

    def cleanup_and_setup(self):
        # setup paths
        video_path = '/home/pishu/Desktop/repos/dpc/test_demo/demo.mp4'
        output_dir = '/home/pishu/Desktop/repos/dpc/test_demo/demo_frames'

        # cleranup
        import shutil
        shutil.rmtree(output_dir)
        from utils import sys_utils as su
        su.create_folder(output_dir)

        # return paths
        return video_path, output_dir

    def test_get_video_information(self):
        video_path, output_dir = self.cleanup_and_setup()
        output = vu.get_video_information(video_path)
        self.assertEqual(output, [29.97002997002997, 28.8288, 864])

    def test_extract_frames(self):
        video_path, output_dir = self.cleanup_and_setup()
        count = vu.get_video_frames(video_path, output_dir, fps = 20)
        self.assertEqual(count, 577)

    def test_extract_frames_simp(self):
        video_path, output_dir = self.cleanup_and_setup()
        count = vu.get_video_frames_simp(video_path, output_dir)
        self.assertEqual(count, 864)

if __name__ == '__main__':
    unittest.main()