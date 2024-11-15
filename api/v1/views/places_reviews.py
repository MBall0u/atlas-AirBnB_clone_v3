#!/usr/bin/python3
"""module for Reviews that interacts with the Review model in the database"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Gets a list of all reviews on the given place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Gets the review with the given ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Gets the review with the given ID on the given place"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    new_review = Review(
        text=data['text'], place_id=place_id, user_id=data['user_id']
    )

    for key, value in data.items():
        if key not in [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at'
        ]:
            setattr(new_review, key, value)

    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes the review with the given ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates the review with the given ID, adding or editing the given data"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at'
        ]:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
