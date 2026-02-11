from fastapi import FastAPI
from .import model
from .database import engine
from .router import product, seller, login

app = FastAPI(title='Product API\'s', description='This api is to build product and seller',
              terms_of_service='https://google.com', contact={
                  'Developer name': 'Gowsik',
                  'email': 'gowsik@gmail.com'
              })


app.include_router(login.router)
app.include_router(product.router)
app.include_router(seller.router)

model.Base.metadata.create_all(engine)
