from PIL import Image
import numpy as np
import os

def return_zeros_width_seg(image_np):
    width_list = []
    height, width = image_np.shape
    for w in range(width):
        if np.all(image_np[:, w] == 0) == True:
            width_list.append(w)

    numbers = width_list

    subsequences = []
    current_subseq = [numbers[0]]

    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i-1] + 1:
            current_subseq.append(numbers[i])
        else:
            subsequences.append(current_subseq)
            current_subseq = [numbers[i]]

    subsequences.append(current_subseq)

    seg_average = []
    for subseq in subsequences:
        average = sum(subseq) / len(subseq)
        seg_average.append(int(average))

    return seg_average

input_dir = 'E:\\CHNCXR_mask\\mask'
output_dir_right = f'{input_dir}_right'
output_dir_left = f'{input_dir}_left'

os.makedirs(output_dir_right, exist_ok=True)
os.makedirs(output_dir_left, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith('.png'):  # Filter for PNG files
        image_path = os.path.join(input_dir, filename)
        image = Image.open(image_path).convert('L')
        image_np = np.array(image)

        right_zero_array = np.zeros(image_np.shape, dtype=image_np.dtype)
        left_zero_array = np.zeros(image_np.shape, dtype=image_np.dtype)

        result = return_zeros_width_seg(image_np)

        print(f"Processing {filename} ...")

        if not len(result) == 3:

            if filename == 'CHNCXR_0066_0_mask.png':
                cutpoint = 1319
            if filename == 'CHNCXR_0141_0_mask.png':
                cutpoint = 1496
            if filename == 'CHNCXR_0636_1_mask.png':
                cutpoint = 1457
            if filename == 'CHNCXR_0650_1_mask.png':
                cutpoint = 1490

        else:

            cutpoint = result[1]

        right_zero_array[0:, :cutpoint] = image_np[0:, :cutpoint]
        left_zero_array[0:, cutpoint:] = image_np[0:, cutpoint:]

        right_mask = Image.fromarray(right_zero_array)
        left_mask = Image.fromarray(left_zero_array)

        right_mask.save(output_dir_right + "\\" + filename)
        left_mask.save(output_dir_left + "\\" + filename)
