#!/usr/bin/env python
# coding: utf-8


import markdown
from os import walk, makedirs, path, listdir
import shutil
from dateutil import parser
from jinja2 import Environment, FileSystemLoader
import schedule
import logging

input_dir = 'blog/publish/'
dist_dir = 'dist/'
static_dir = 'static/'
output_blog_dir = 'dist/posts/'
output_asstes_dir = 'dist/assets/'
html_templates_dir = 'templates/'

#relative path to assets from blogs
rel_path_assets_blog = '../assets/'

valid_asset_file_extension = ('.png', '.jpg', '.jpeg')



def file_to_html(input_path, output_path):
    markdown.markdownFromFile(
        input=input_path,
        output=output_path,
        encoding='utf8',
    )

def generate_posts():

    root = path.dirname(path.abspath(__file__))
    env = Environment( loader = FileSystemLoader(html_templates_dir) )
    posts_template = env.get_template('posts.html.j2')
    post_template = env.get_template('post.html.j2')


    posts_files = []
    posts_dirs = []

    #get list of files and dirs in input_dir
    for (dirpath, dirnames, filenames) in walk(input_dir):
        posts_files.extend(filenames)
        posts_dirs.extend(dirnames)
        break
    
    #delete output dir and create empty one (reset dist)
    shutil.rmtree(dist_dir, ignore_errors=True)
    makedirs(output_blog_dir, exist_ok=True)
    makedirs(output_asstes_dir, exist_ok=True)

    #dict for storing all posts meta data (date + time)
    posts = []

    #posts without assets (as single files)
    for f in posts_files:
        #create paths
        input_path = input_dir + f
        
        post = {}
        temp = f.split('_', 1)
        
        #parse date from file name
        post['date'] = parser.parse(temp[0]).strftime("%d.%m.%Y")
        #parse title from first header in file
        file_content = ""
        with open(input_path, 'r') as file:
            file_content = file.read()
            post["title"] = file_content.split("\n")[0][2:]

        filename = f.rsplit('.', 1)[0]
        #save filename for generating links
        post['filename'] = filename
        
        #new output file path
        output_path = output_blog_dir + filename + '.html'
        #transpile
        html = markdown.markdown(file_content, extensions=['fenced_code'])
        #file_to_html(input_path, output_path)
        with open(output_path, 'w') as file:
            file.write(post_template.render(
                post = html,
            ))
        posts.append(post)
        

    #posts with assets (in folders)
    for d in posts_dirs:
        #temp dict for storing assets path changes
        asset_paths = {}
        
        #create paths
        input_path = input_dir + d + '/'
        output_path = output_blog_dir + d + '/'

        #iterate through input_path
        for root, dirs, files in walk(input_path):
            for file in files:
                # copy all assets
                if file.endswith(valid_asset_file_extension):
                    i_path = input_path + file
                    o_path = output_asstes_dir + file
                    shutil.copyfile(i_path, o_path)
                    #store original path an d
                    asset_paths[file] = rel_path_assets_blog +  file
                    
                # transpile all md into html and put to output_blog_dir
                if file.endswith(".md"):
                    i_file_path = input_path + file
                    post = {}
                    try:
                        date_temp = file.split('_', 1)
                    except AttributeError as a_error:
                        logging.warn("Could get raw date string for " + file)
                        continue

                    #parse date from file name
                    post['date'] = parser.parse(date_temp[0]).strftime("%d.%m.%Y")
                    #parse title from first header in file
                    with open(i_file_path, 'r') as f:
                        content = f.read()
                        post["title"] = content.split("\n")[0][2:]
                    
                    filename = file.rsplit('.', 1)[0]
                    #save filename for generating links
                    post['filename'] = filename

                    #new output file path
                    o_file_path = output_blog_dir + filename + '.html'
                    
                    file_to_html(i_file_path, o_file_path)
                    #replace the assetes path with new assets path
                    with open(o_file_path, 'r') as f :
                        filedata = f.read()

                    for original_path in asset_paths:
                        filedata = filedata.replace(original_path, asset_paths[original_path])

                    # Write the file out again with jinja template this time
                    with open(o_file_path, 'w') as f:
                        f.write(post_template.render(
                            post = filedata,
                        ))

                    posts.append(post)
                    logging.info("created post with title: " + post['title'])

                    
    posts.sort(key=lambda x: x["date"], reverse=True)

    #generate posts overview page
    with open(dist_dir + 'posts.html', 'w') as fh:
        fh.write(posts_template.render(
            posts = posts,
        ))
    return posts


def copy_static_files():
    src_files = listdir(static_dir)
    for file_name in src_files:
        full_file_name = path.join(static_dir, file_name)
        if path.isfile(full_file_name):
            shutil.copy(full_file_name, dist_dir)

def scheduled():
    posts = generate_posts()
    print(posts)
    copy_static_files()


if __name__ == "__main__":

    schedule.every(1).minutes.do(scheduled)
    #run initialy
    scheduled()
    while True:
        schedule.run_pending()
