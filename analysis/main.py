import os 
import json
import numpy as np
import pandas as pd 
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.image as img 

src_data_path = '../../study output/'


def import_participant_prompts(participant_id, task):
    with open(os.path.join(src_data_path, str(participant_id), task, '{} {}.json'.format(task, participant_id))) as f:
        data = json.load(f)
        return data 


def get_task_prompts(task):
    prompts = []
    for root, dirs, files in os.walk(src_data_path):
        if task in root:
            for f in files:
                if '.json' in f:
                    data = json.load(open(os.path.join(root, f)))
                    for d in data:
                        prompts.append(d['prompt'])
    return prompts

def prompts_metrics():
    # data structure, only one metric for now: 'prompt_length'
    data = {'participant': [], 
            'task': [], 
            'trial': [], 
            'prompt_length': []}
    
    # browse file system 
    for root, dirs, files in os.walk(src_data_path):
        for f in files:
            if '.json' in f:
                p_id = root.split('/')[-2]
                t_id = root.split('/')[-1]
                json_data = json.load(open(os.path.join(root, f)))
                
                # sort the data pert image name to get the right order 
                # at which images have been generated: 
                image_ids = np.argsort([l['image'] for l in json_data])
                json_data = np.array(json_data)[image_ids]
                
                # fill the data structure
                for di, d in enumerate(json_data):
                    data['participant'].append(p_id)
                    data['task'].append(t_id)
                    data['trial'].append(di+1)
                    data['prompt_length'].append(len(d['prompt']))
    return data


def display_participant_image_prompt(participant_id, task, image_n):
    data = import_participant_prompts(participant_id, task)
    all_image_ids = sorted([l['image'] for l in data])
    image_id = all_image_ids[image_n]
    # get image and corresponding prompt
    image_toplot = img.imread(os.path.join(src_data_path,
        str(participant_id), task, 'img', '{}.png'.format(image_id))) 
    for l in data:
        if l['image'] == image_id:
            prompt_toplot = l['prompt']
    # display 
    imgplot = plt.imshow(image_toplot)
    plt.title('{}'.format(prompt_toplot))
    plt.show()





display_participant_image_prompt(2, 'story', 4)
# prompts = get_task_prompts('story')
data = prompts_metrics()

data_df = pd.DataFrame(data)
sns.barplot(data_df, x="trial", y="prompt_length", hue='task')
plt.show()

