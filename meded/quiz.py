import sqlite3
import random
from flask import g, url_for
from meded import query_db, commit_db, lastid_db
from meded import constants

def getNormalQuiz():
	normalImageCount = int(query_db('SELECT COUNT(images.image_id) FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id', (constants.NORMAL_IMAGE_TAG,), True))

	normalResult = query_db('SELECT image_id, filename FROM images OFFSET ?', (random.randint(0, normalImageCount - 1)), True)

	abnormalImageCount = int(query_db('SELECT COUNT(images.image_id) FROM images, image_tags, links_tag_to_image WHERE image_tags.value=? AND image_tags.image_tag_id=links_tag_to_image.image_tag_id AND links_tag_to_image.image_id=images.image_id', (constants.ABNORMAL_IMAGE_TAG,), True))

	abnormalResult = query_db('SELECT image_id, filename FROM images OFFSET ?', (random.randint(0, abnormalImageCount - 1)), True)


	response = {"normal":{"image_id":normalResult[0], "image_loc":url_for(normalResult[1])}, {"abnormal":{"image_id":abnormalResult[0], "image_loc":url_for(abnormalResult[1])}}}
	return response