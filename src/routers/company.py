
from fastapi import APIRouter, Request
from src.misc.constants.messages import DATABASE_CONNECTION_ERROR, OK
from src.utilities.utils import dataFrameToJsonObject, get_error_message, company_details, company_datasets

router = APIRouter(
    prefix="/company",
    tags=["Company"]
    )

@router.get('/details')
def get_details():
    try:
        dataset = company_details.to_dict()
        
        if dataset :
            return {
                'success': True, 
                'message': OK, 
                'data': dataset, 
                'user_wallets': dataFrameToJsonObject(company_datasets['rs1']),
                'franchise_wallets': dataFrameToJsonObject(company_datasets['rs2']),
                'incomes_list': dataFrameToJsonObject(company_datasets['rs3']),
                'packages': dataFrameToJsonObject(company_datasets['rs4'])
                }
            
        return {'success': False, 'message': DATABASE_CONNECTION_ERROR }
    except Exception as e:
        print(e.__str__())
        return {'success' : False, 'message' : get_error_message(e)}
    
