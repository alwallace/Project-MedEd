import sqlite3
import random
from flask import g, url_for
from meded import app
from meded import query_db, commit_db, lastid_db
from meded import constants

def getNormalQuiz():
	normalImageCount = int(query_db('SELECT COUNT(images.image_id) FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id', (constants.NORMAL_IMAGE_TAG,), True)[0])

	normalResult = query_db('SELECT images.image_id, images.filename FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id LIMIT 1 OFFSET ' + str(random.randint(0, normalImageCount - 1)), (constants.NORMAL_IMAGE_TAG,), True)

	abnormalImageCount = int(query_db('SELECT COUNT(images.image_id) FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id', (constants.ABNORMAL_IMAGE_TAG,), True)[0])

	abnormalResult = query_db('SELECT images.image_id, images.filename FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id LIMIT 1 OFFSET ' + str(random.randint(0, abnormalImageCount - 1)), (constants.ABNORMAL_IMAGE_TAG,), True)


	response = {"normal":{"image_id":normalResult[0], "image_loc":url_for('static', filename='images/'+normalResult[1]) }, 
			   "abnormal":{"image_id":abnormalResult[0], "image_loc":url_for('static', filename='images/'+abnormalResult[1]) }}
	return response