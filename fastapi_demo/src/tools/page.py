"""分页相关"""

from tortoise.queryset import QuerySet


def make_page(queryset: QuerySet, *, cur_page: int, page_size: int) -> QuerySet:
    """分页

    :param queryset: QuerySet
    :param cur_page: 当前页号
    :param page_size: 每页显示数量
    """
    return queryset.offset((cur_page - 1) * page_size).limit(page_size)


async def get_para(request):

    query_params = request.query_params
    print(query_params, "xxxx")
    result_data = await request.body()
    print(result_data)
    if query_params:
        return query_params
    else:
        return result_data.decode()