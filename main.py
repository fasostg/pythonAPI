from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Configura o caminho a ser salvo o banco de dados. Exemplo: para salvar em uma pasta 'temp', use 'sqlite:///temp/database.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# O modelo é o que estrutura nosso BD, definindo as colunas que formarão a "tabela" VideoModel
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

# O create_all() é usado uma única vez, se não o banco de dados sofrerá overwritten
#db.create_all()

# Cria os argumentos que deverão ser passados através de uma requisição
video_post_args = reqparse.RequestParser()
video_post_args.add_argument("name", type=str, help="O nome está incorreto!", required=True)
video_post_args.add_argument("views", type=int, help="O número de views está incorreto!", required=True)
video_post_args.add_argument("likes", type=int, help="O número de likes está incorreto!", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="O nome está incorreto!")
video_update_args.add_argument("views", type=int, help="O número de views está incorreto!")
video_update_args.add_argument("likes", type=int, help="O número de likes está incorreto!")

# Em conjunto com o @marshal_field(), o resource_fields garante que, ao usar um GET, o usuário receba de retorno os campos definidos abaixo
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    # Quando receber o retorno do objeto VideoModel (ao usar o GET), o marshal_with() serializa esse objeto em um JSON
    @marshal_with(resource_fields)
    # Requisição GET para consulta dos dados no banco
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video não encontrado!!")
        return result

    @marshal_with(resource_fields)
    # Requisição POST para inserção de novos dados no banco
    def post(self, video_id):
        # A função parse_args() é responsável por coletar todos os dados definidos anteriormente com o add_argument()
        args = video_post_args.parse_args()
        
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="O ID desse vídeo já existe!!")
        
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        db.session.delete(result)
        db.session.commit()
        return 'Removido com sucesso!', 204

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_update_args.parse_args()
        
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="O ID do vídeo especificado não existe, não é possível atualizar!!")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
