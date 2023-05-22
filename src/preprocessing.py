import os
import time


def check_program_completion(program_path, output_files, max_wait_time=60000, interval=10, skip_program=False):
    """
    检查程序是否已完成
    :param program_path: 程序路径，包括文件名与参数
    :param output_files: 程序执行后需要生成的输出文件
    :param max_wait_time: 最大等待时间，单位为秒，默认为60000秒
    :param interval: 等待间隔时间，单位为秒，默认为10秒
    :param skip_program: 是否跳过程序执行，默认为False
    :return: True表示程序已完成，False表示程序未完成或超时
    """
    if skip_program:
        print(f'Skipping {program_path}...')
        return True

    start_time = time.time()
    program_finished = False
    while not program_finished and time.time() - start_time < max_wait_time:
        os.system(program_path)
        output_files_exist = all([os.path.exists(file) for file in output_files])
        if output_files_exist:
            program_finished = True
        else:
            #print('waiting for {} to finish...'.format(program_path))
            time.sleep(interval)
    if program_finished:
        print('{} finished.'.format(program_path))
    else:
        print('{} failed to finish within the given time.'.format(program_path))
    return program_finished


def main():
    dualsheet_program_path = 'root\\src\\preprocessing\\dualsheet.py'
    dualsheet_output_files = ['root\\data\\raw_data\\LP11_processed.xlsx']
    disassemble_program_path = 'root\\src\\preprocessing\\disassemble.py'
    disassemble_output_files = ['root\\data\\cleaned_data\\9.62 order run up_frames.xlsx',
                                'root\\data\\cleaned_data\\9.62 order run down_frames.xlsx',
                                'root\\data\\cleaned_data\\26 order run up_frames.xlsx',
                                'root\\data\\cleaned_data\\26 order run down_frames.xlsx']
    preprocessing_program_path = 'root\\src\\preprocessing\\preprocessingdone.py'
    preprocessing_output_files = ['root\\result\\rds_value\\9.62 order run up_frames_results.xlsx',
                                   'root\\result\\rds_value\\9.62 order run down_frames_results.xlsx',
                                   'root\\result\\rds_value\\26 order run up_frames_results.xlsx',
                                   'root\\result\\rds_value\\26 order run down_frames_results.xlsx']

    # 检查 dualsheet.py 是否需要执行，如果已生成对应的文件，则跳过执行
    dualsheet_skip = all([os.path.exists(file) for file in dualsheet_output_files])
    dualsheet_finished = check_program_completion(dualsheet_program_path, dualsheet_output_files, skip_program= dualsheet_skip)

    # 检查 disassemble dualsheet.py 是否需要执行，如果已生成对应的文件，则跳过执行
    disassemble_skip = all([os.path.exists(file) for file in disassemble_output_files])
    disassemble_finished = check_program_completion(disassemble_program_path, disassemble_output_files,
                                                    skip_program=disassemble_skip)

    # 检查 preprocessing done.py 是否需要执行，如果已生成对应的文件，则跳过执行
    preprocessing_skip = all([os.path.exists(file) for file in preprocessing_output_files])
    preprocessing_finished = check_program_completion(preprocessing_program_path, preprocessing_output_files,
                                                       skip_program=preprocessing_skip)

    if preprocessing_finished:
        print('Data preprocessing completed successfully!')
    else:
        print('Data preprocessing failed to complete within the given time.')


if __name__ == '__main__':
    main()