nndata_dir = './tmp_data/extracted/'
dnn_file = './tmp_data/all-data.npz'
file_ext = '.npy|.npz|.NPY|.NPZ|'
marked_file_dir = '/media/sheldon/文档/All_result/final_result/'
sep_file_dir='/media/sheldon/文档/All_result/final_result/'
sep_file_ext='.npz|.NPZ'
data_file_dir = '/media/sheldon/文档/All_result/data_result/'
data_file_ext='.npz|.NPZ'
train_data_file = './tmp_data/filted-train-data.npz'
test_data_file = './tmp_data/test-data.npz'
all_data_file = './tmp_data/filted-data.npz'
# train parms
n_epoch = 500
batch_size_train = 10
batch_size_val = 50
radio = 0.6
alpha = 0.139

# save parms
max_to_keep = 5
