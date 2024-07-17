from pydantic import BaseModel

from src.misc.constants import VALIDATORS


class AddCategory_Request(BaseModel):
    parent_id: int = 0
    name: str
    can_have_subcategories: bool = False


class GetCategories_Request(BaseModel):
    name: str = ''
    date_from: str=''
    date_to: str=''
    parent_id: int=0
    all: bool=False
    page_index: int
    page_size: int


class UpdateCategory_Request(BaseModel):
    category_id: int
    name: str = ''
    parent_id: int = 0


class AddUpdateProduct_Request(BaseModel):
    product_id: int
    category_id: int
    product_name: str = ''
    product_image: str = ''
    hsn: str = ''
    bv: float
    mrp: float
    discount_percentage: float
    gst_percentage: float
    description: str


class GetProducts_Request(BaseModel):
    product_id: int=0
    category_id: int=0
    name: str = ''
    date_from: str=''
    date_to: str=''
    page_index: int
    page_size: int


class AddProductStock_Request(BaseModel):
    product_id: int=0
    quantity: int=0
    remarks: str = ''


class GetProductStockTransactions_Request(BaseModel):
    product_id: int=0
    category_id: int=0
    remarks: str = ''
    date_from: str=''
    date_to: str=''
    page_index: int
    page_size: int


class AddShippingAddress(BaseModel):
    user_id: str = VALIDATORS.USER_ID
    user_type: str = VALIDATORS.USER_TYPE
    name: str
    address: str
    district: str
    state: int
    country: int
    pin_code: str = VALIDATORS.PIN_CODE
    mobile_no: str = VALIDATORS.MOBILE_NO


class PlaceRepurchaseOrder(BaseModel):
    to_user_id: str
    to_user_type: str
    shipping_charges: float
    products: list
    payment_id: str = ''
    is_paid: bool
    is_dispatched: bool
    dispatch_mode: str
    courier_name: str
    courier_url: str
    courier_tracking_number: str
    shipping_address_id: int
    wallet_id: int


class GetRepurchaseOrders(BaseModel):
    order_number: int
    user_id: str
    user_type: str
    by_franchise_id: str
    date_from: str=''
    date_to: str=''
    payment_mode: str
    reference_no: str
    dispatch_status: str
    paid_status: str
    type: str = 'To Me'
    order_id: int = 0
    page_index: int = 0
    page_size: int = 100


class RepurchaseOrderDispatchStatusUpdateRequest(BaseModel):
    order_id: int
    status: str = VALIDATORS.PIN_PRODUCT_DISPATCH_STATUS_UPDATE
    dispatched_through: str
    courier_name: str
    courier_url: str
    courier_tracking_number: str
    remarks: str = ''
