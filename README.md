# BudgetAPI
Application allow for creating user accounts. Users are authenticated via JWT Authentication tokens. Each user can create `Budgets` and share it with any number of other users. The `Budget` consists of `CashFlows` (incomes or expenses). They can be grouped into categories `CashFlowCategories` witch belongs to `Budget`.

Project is still under development. Not all functionalities are covered by unit tests yet. 

## Run application

#### Clone repository
```
git clone https://github.com/matemiro/WeatherAPI.git
```
#### Environment variables
Create `.env` file in main folder with environment variables according to `.env-sample` file.

#### Run docker containers
```
sudo docker-compose up
```
#### Application is running on 
```
 http://127.0.0.1:8001/
```
#### Running tests
Check docker web container (`budgetapi_web`) id (`CONTAINER ID`) using command:
```
sudo docker ps
```
Run tests using command:
```
 sudo docker exec -t {CONTAINER ID} pytest -vs app/tests/tests.py users/tests/tests.py
```


## Endpoints

#### Permissions:
- Any user can create budget.
- Only budget **creator** can share it to another user.
- Adding/updating categories or cash flows requires being budget **creator** *or* having **editor** role.

- Retrieving objects details requires being budget **creator** *or* having **editor**/**read only** role.

<br>

| Method  | Endpoint                           | Description                                                                                                                             | Parameters (*required)                                                                                                                         |
|---------|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `POST`  | `/register/`                       | Create new account                                                                                                                      | `username`* , `password`*, `email`                                                                                                             |
| `POST`  | `/api/token/`                      | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. | `username`* , `password`*, `email`                                                                                                             |
| `POST`  | `/api/token/refresh/`              | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.                            | `refresh`* (refresh token)                                                                                                                     |
| `POST`  | `/api/token/verify/`               | Takes a token and indicates if it is valid. This view provides no information about a token's fitness for a particular use.             | `token`*                                                                                                                                       |
| `GET`   | `/budgets/`                        | List all user's budgets                                                                                                                 | -                                                                                                                                              |
| `POST`  | `/budgets/`                        | Create new budget                                                                                                                       | `name`*, `description`                                                                                                                         |
| `GET`   | `/budgets/{budget_id}/`            | Retrieve budget details                                                                                                                 | -                                                                                                                                              |
| `PUT`   | `/budgets/{budget_id}/`            | Update budget object                                                                                                                    | `name`*, `description`                                                                                                                         |
| `PATCH` | `/budgets/{budget_id}/`            | Partial update budget object                                                                                                            | `name`, `description`                                                                                                                          |
| `DEL`   | `/budgets/{budget_id}/`            | Delete budget object                                                                                                                    | -                                                                                                                                              |
| `GET`   | `/categories/?budget={budget_id}/` | List categories in budget object                                                                                                        | `budget`* (id of budget object)                                                                                                                |
| `POST`  | `/categories/`                     | Create new category                                                                                                                     | `budget`* (id of budget object), `name`* (category name), `description`                                                                        |
| `GET`   | `/categories/{category_id}/`       | Retrieve category object                                                                                                                | -                                                                                                                                              |
| `PUT`   | `/categories/{category_id}/`       | Update category object                                                                                                                  | `name`* (category name), `description`                                                                                                         |
| `PATCH` | `/categories/{category_id}/`       | Partial update category object                                                                                                          | `name` (category name), `description`                                                                                                          |
| `DEL`   | `/categories/{category_id}/`       | Delete category object                                                                                                                  | -                                                                                                                                              |
| `GET`   | `/cash-flows/?budget={budget_id}/` | List cash flows in budget                                                                                                               | `budget`* (id of budget object)                                                                                                                |
| `POST`  | `/cash-flows/`                     | Create cash flow in budget                                                                                                              | `budget`* (id of budget object), `amount`* , `name`* (cash flow name), `type`* (1: income, 2: expense),  `description` (cash flow description) |
| `GET`   | `/cash-flows/{cashflow_id}/`       | Retrieve cash flow object                                                                                                               | -                                                                                                                                              |
| `PUT`   | `/cash-flows/{cashflow_id}/`       | Update cash flow object                                                                                                                 | `amount`* , `name`* (cash flow name), `type`* (1: income, 2: expense),  `description` (cash flow description)                                  |
| `PATCH` | `/cash-flows/{cashflow_id}/`       | Partial update cash flow object                                                                                                         | `amount`, `name` (cash flow name), `type` (1: income, 2: expense),  `description` (cash flow description)                                      |
| `DEL`   | `/cash-flows/{cashflow_id}/`       | Delete cash flow object                                                                                                                 | -                                                                                                                                              |
| `POST`  | `/budget-share/`                   | Share budget to another user                                                                                                            | `budget`* (id of budget object), `shared_with`* (id of user), `role`* (1: editor, 2: read-only)                                                |
| `PUT`   | `/budget-share/{budget_share_id}/` | Update budget share with `budget_share_id`                                                                                              | `budget`* (id of budget object), `shared_with`* (id of user), `role`* (1: editor, 2: read-only)                                                |
| `PATCH` | `/budget-share/{budget_share_id}/` | Change role of sharing                                                                                                                  | `role`* (1: editor, 2: read-only)                                                                                                              |
| `DEL`   | `/budget-share/{budget_share_id}/` | Unshare the budget                                                                                                                      | -                                                                                                                                              |