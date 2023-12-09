from flask import Blueprint
from Controller.Controller import Controller

router = Blueprint('interpreter', __name__)
controller = Controller()

@router.route('/')
def running():
    return controller.running()