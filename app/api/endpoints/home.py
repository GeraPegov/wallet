from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates('app/api/endpoints/templates')

@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name='form.html', 
        context={'request': request}
    )
