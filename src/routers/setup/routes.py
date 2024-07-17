
from fastapi import APIRouter

from src.data_access.setup import routes as data_access
from src.misc.constants.messages import (DATABASE_CONNECTION_ERROR)
from src.misc.helpers.helper_utils import generate_routes_json
from src.schemas.Setup import AddRoute, UpdateActiveRoutes
from src.utilities.utils import get_error_message

router = APIRouter()


@router.post('/add_edit_route')
async def add_edit_route(req: AddRoute):
    try:
        dataset = data_access.add_edit_route(req=req)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                generate_routes_json()
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.delete('/delete_route')
async def delete_route(id: int):
    try:
        dataset = data_access.delete_route(id=id)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                generate_routes_json()
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}


@router.put('/update_active_routes')
async def update_active_routes(req: UpdateActiveRoutes):
    try:
        dataset = data_access.update_active_routes(user_type=req.user_type, route_ids=req.route_ids)
        # print(dataset)
        if len(dataset) > 0 and len(dataset['rs']):
            ds = dataset['rs']
            if ds.iloc[0].loc["success"]:
                generate_routes_json()
                return {'success': True, 'message': ds.iloc[0].loc["message"]}

            return {'success': False, 'message': ds.iloc[0].loc["message"]}

        return {'success': False, 'message': DATABASE_CONNECTION_ERROR}

    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}
