from src.controllers.auth_controller import auth
from src.controllers.checklists_controller import checklists
from src.controllers.items_controller import items


registerable_controllers = [
    auth,
    checklists,
    items
]
