from bucketList.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from bucketList.models import Bucketitems, db
# from flasgger import swag_from
from bucketList.models import Bucketitems 
import datetime 


buckets = Blueprint("buckets", __name__, url_prefix="/api/v1/buckets" )

# Create a new bucket list
@buckets.route('/bucketlists/', methods = ['POST', 'GET'])
@jwt_required()
def handle_bucketitems():
    user_id = get_jwt_identity()

    if request.method == 'POST':
        
        name = request.json['name']
        description = request.json['description']
        completed = request.json['completed']
        created_by = request.json['created_by']

        

        if Bucketitems.query.filter_by(id=id).first():
            return jsonify({
                'error': 'Bucket already exists'
            }), HTTP_409_CONFLICT

        bucketitem = Bucketitems(name=name, description=description, completed=completed, created_by=user_id)
        db.session.add(bucketitem)
        db.session.commit()

        return jsonify({
            'id': bucketitem.id,
            'name': bucketitem.name,
            'description': bucketitem.description,
            'completed': bucketitem.completed,
            'created_by' : bucketitem.created_by,
            'created_at': bucketitem.created_at,
            'updated_at': bucketitem.updated_at,
        }), HTTP_201_CREATED

    else:
        # page Pergination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        buckets = Bucketitems.query.filter_by(created_by=user_id).paginate(page=page, per_page=per_page)

        data = []

        for bucket in buckets.items:
            data.append({
            'id': bucket.id,
            'name': bucket.name,
            'description': bucket.description,
            'completed': bucket.completed,
            'created_at': bucket.created_at,
            'updated_at': bucket.updated_at,
        })

    # return jsonify({'data': data}), HTTP_200_OK
    
    meta = {
            "page": buckets.page,
            'pages': buckets.pages,
            'total_count': buckets.total,
            'prev_page': buckets.prev_num,
            'next_page': buckets.next_num,
            
        }

    return jsonify({'data': data, "meta": meta}), HTTP_200_OK   

#retriving a single bucket
@buckets.get("/bucketlists/<id>")
@jwt_required()
def get_bucket(id):
    user_id = get_jwt_identity()

    bucket = Bucketitems.query.filter_by(created_by=user_id, id=id).first()

    if not bucket:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    return jsonify({
        'id': bucket.id,
        'name': bucket.name,
        'description': bucket.description,
        'completed': bucket.completed,
        'created_at': bucket.created_at,
        'updated_at': bucket.updated_at,
    }), HTTP_200_OK

   
@buckets.patch('/bucketlists/<id>')
@jwt_required()
def editbucket(id):
    user_id = get_jwt_identity()

    bucket = Bucketitems.query.filter_by(created_by=user_id, id=id).first()

    if not bucket:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    name = request.json['name']
    description = request.json['description']
    completed = request.json['completed']
    

    bucket.name = name
    bucket.description = description
    bucket.completed = completed
    

    bucket.save()

    return jsonify({
        'id': bucket.id,
        'name': bucket.name,
        'description': bucket.description,
        'completed': bucket.completed,
        'created_at': bucket.created_at,
        'updated_at': bucket.updated_at,
    }), HTTP_200_OK



@buckets.delete("/bucketlists/<id>")
@jwt_required()
def delete_buckt(id):
    user_id = get_jwt_identity()

    bucket = Bucketitems.query.filter_by(created_by=user_id, id=id).first()

    if not bucket:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    bucket.delete()

    return jsonify({"message" : "Item Deleted"}), HTTP_204_NO_CONTENT