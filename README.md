# fastapi_demo_project

#### 介绍
听说你觉得django没有异步，玩起来不高大上。很好，我想教你用django的方式写fastapi,隔壁老奶奶用的都比你6。
1. fastapi可以实现异步，确实比django要自由很多，但是自由的代价肯定是开发时间换来的。本人是个django重度使用者，但是要学会在合适的时机选择合适的框架。orm太香了，所以研究了这一套
2. 这个项目的数据库和我上个django项目是同一个，详情可以参考[django_open_project](https://github.com/haiweifeng/github_django_demo_project)
3. 本项目的中心思想是用django的方式写fastapi，主要从model层的替换和数据的操作方面，和django的区别很小，很多django的代码粘贴过来改动一下可以直接用
4. 固定的开发套路可以降低开发成本，就算减少不了代码量，但是可以和同事建立一样的开发习惯，有利于团队协作


#### 写在前边的一些看法

1.  要说fastapi比django快，也只能说是相对的。前边说过所有耗时的操作都在数据库，在100万条和1000万条数据的测试上来看，fastapi在百万数据上并不占据优势，反而在第一次请求时比django慢，
但是tortoise在查询上应该是做了缓存优化的。在千万数据层面fastapi是有些许优势的。但是就搞个破后台，数据量大了以后再优化呗，总不能一步到位不给别人活路了吧。

2.  在写请求的时候我用了好几种书写方式，主要是为了让有需要的同学快速上手。模仿着写几个肯定就会了，主要还是请求方式，参数上的区别。可以参考fastapi官方文档
写的非常详细。[官方文档](https://fastapi.tiangolo.com/zh/)
3.  我在项目中也加了mq的监听和定时任务的配置，按需取用。

#### 使用说明

1.  因为没有了类视图，所以就不能有继承的思路了。但是我们可以做到curd在设计上格式统一。
```python
@router.post("/user_list/", summary='用户列表展示',response_model=UsersResp)
async def user_list(
                   phone: str = Form(description='phone', default=""),
                   name: str = Form(description='name', default=""),
                   pageSize: int = Form(description='条数', default=20,le=100),
                   pageNumber: int = Form(description='页码', default=1),
                   ):
    search = {"phone": phone, 'name': name}
    data, total = await Users.query_by_search(search, page_size=pageSize, cur_page=pageNumber)

    res = {'data': data, 'page_size': pageSize, "cur_page": pageNumber, 'total': total}
    return resp_200_lis(data=res, msg='success')
```
标准列表页返回格式写法，用过的都说好，主要逻辑都在query_by_search里，也能满足大部分需求，特殊逻辑等数据返回了自己加就是了，增加，编辑，删除就不用说了，直接看完就能上手。
2. fastapi的参数优势，自带了参数校验，不像我搞的django还得自己写判断逻辑。详情参考官方文档。
3. fastapi的中间件,注意这个中间件，在请求返回之后，在请求返回之前，可以做些操作，比如记录请求时间，或者做权限校验等等。
```python
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    # 进入请求前处理
    if not [1 for w in NO_TOKEN_URL_LIST if w in request.url.__str__()]:
        sts = await check_token(request.headers.get('token',""))
        if not sts:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    'code': 1000,
                    'message': 'token异常！',
                    'data': {},
                }
            )
    response = await call_next(request)
    # 请求返回之后的处理
    process_time = time.time() - start_time

    response.headers["X-Use-Time"] = str(process_time)
    print("请求时间：", process_time)
    return response
```
4. 有很多有趣的功能或者设计，我注释了。你可以放开自己探索一下


5. 关于部署
环境包参考req.txt文件，使用supervisor部署项目，配置文件参考supervisor_conf中的配置文件。如果你不会用可以留言，我写个详细的教程

### 联系我
微信：harwen001 
如果有什么问题，欢迎留言交流，或者加我微信，一起学习。你要是真觉得这个项目帮助了你，也可以请我喝杯咖啡。![码在这](fastapi_demo/media/1.jpg)