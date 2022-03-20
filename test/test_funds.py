from numpy import dtype
from pandas import CategoricalDtype

from fipiran.funds import Fund, dependency_graph_data, funds, average_returns, map_data
from . import patch_session


fund = Fund(11215)


def test_repr():
    assert repr(fund) == 'Fund(11215)'
    assert repr(Fund('11215')) == "Fund('11215')"


@patch_session('getfundchartasset_atlas.json')
async def test_asset_allocation():
    d = await fund.asset_allocation()
    del d['fiveBest']
    assert sum(d.values()) > 99.99


@patch_session('getfundchart_atlas.json')
async def test_issue_cancel_history():
    df = await fund.issue_cancel_history(all_=False)
    assert [*df.dtypes.items()] == [
        ('issueNav', dtype('float64')),
        ('cancelNav', dtype('float64')),
        ('statisticalNav', dtype('float64'))]
    assert len(df) >= 365
    assert df.index.name == 'date'
    assert df.index.dtype == '<M8[ns]'


@patch_session('getfundnetassetchart_atlas.json')
async def test_nav_history():
    df = await fund.nav_history(all_=False)
    assert [*df.dtypes.items()] == [
        ('netAsset', dtype('int64')),
        ('unitsSubDAY', dtype('int64')),
        ('unitsRedDAY', dtype('int64')),
    ]
    assert len(df) >= 365
    assert df.index.dtype == '<M8[ns]'


@patch_session('getfund_atlas.json')
async def test_info():
    info = await fund.info()
    assert len(info) >= 63
    assert type(info) is dict


@patch_session('fundcompare.json')
async def test_funds():
    df = await funds()
    assert len(df) > 300
    assert [*df.dtypes.items()] == [
        ('regNo', dtype('int64')),
        ('name', 'string'),
        ('rankOf12Month', dtype('int64')),
        ('rankOf36Month', dtype('int64')),
        ('rankOf60Month', dtype('int64')),
        ('rankLastUpdate', dtype('O')),
        ('fundType', dtype('int64')),
        (
            'typeOfInvest',
            CategoricalDtype(
                categories=['IssuanceAndCancellation', 'Negotiable'], ordered=False
            ),
        ),
        ('fundSize', dtype('float64')),
        ('initiationDate', dtype('O')),
        ('dailyEfficiency', dtype('float64')),
        ('weeklyEfficiency', dtype('float64')),
        ('monthlyEfficiency', dtype('float64')),
        ('quarterlyEfficiency', dtype('float64')),
        ('sixMonthEfficiency', dtype('float64')),
        ('annualEfficiency', dtype('float64')),
        ('statisticalNav', dtype('float64')),
        ('efficiency', dtype('float64')),
        ('cancelNav', dtype('float64')),
        ('issueNav', dtype('float64')),
        ('dividendIntervalPeriod', dtype('float64')),
        ('guaranteedEarningRate', dtype('float64')),
        ('date', dtype('<M8[ns]')),
        ('netAsset', dtype('float64')),
        ('estimatedEarningRate', dtype('float64')),
        ('investedUnits', dtype('float64')),
        ('articlesOfAssociationLink', dtype('O')),
        ('prosoectusLink', dtype('O')),
        ('websiteAddress', dtype('O')),
        ('manager', 'string'),
        ('managerSeoRegisterNo', 'Int64'),
        ('auditor', 'string'),
        ('custodian', 'string'),
        ('guarantor', 'string'),
        ('beta', dtype('float64')),
        ('alpha', dtype('float64')),
        ('isCompleted', dtype('bool')),
        ('fundWatch', dtype('O')),
    ]


@patch_session('MFBazdehAVG.html')
async def test_average_returns():
    df = await average_returns()
    assert len(df) == 4
    assert [*df.dtypes.items()] == [
        ('نوع صندوق', dtype('O')),
        ('خالص ارزش دارایی صندوق(میلیارد ریال)', dtype('int64')),
        ('%میانگین دارایی\u200cهای نقدی', dtype('float64')),
        ('میانگین بازدهی هفته(%)', dtype('float64')),
        ('میانگین بازدهی ماه(%)', dtype('float64')),
        ('میانگین بازدهی 3 ماهه(%)', dtype('float64')),
        ('میانگین بازدهی 6 ماهه(%)', dtype('float64')),
        ('میانگین بازدهی سال(%)', dtype('float64')),
        ('میانگین بازدهی از آغاز فعالیت(%)', dtype('float64')),
    ]


@patch_session('treemap.json')
async def test_map_data():
    df = await map_data()
    assert [*df.dtypes.items()] == [
        ('regNo', dtype('int64')),
        ('name', 'string[python]'),
        ('rankOf12Month', dtype('int64')),
        ('rankOf36Month', dtype('int64')),
        ('rankOf60Month', dtype('int64')),
        ('rankLastUpdate', dtype('O')),
        ('fundType', dtype('int64')),
        (
            'typeOfInvest',
            CategoricalDtype(
                categories=['IssuanceAndCancellation', 'Negotiable'], ordered=False
            ),
        ),
        ('fundSize', dtype('int64')),
        ('initiationDate', dtype('<M8[ns]')),
        ('dailyEfficiency', dtype('float64')),
        ('weeklyEfficiency', dtype('float64')),
        ('monthlyEfficiency', dtype('float64')),
        ('quarterlyEfficiency', dtype('float64')),
        ('sixMonthEfficiency', dtype('float64')),
        ('annualEfficiency', dtype('float64')),
        ('statisticalNav', dtype('O')),
        ('efficiency', dtype('float64')),
        ('cancelNav', dtype('float64')),
        ('issueNav', dtype('float64')),
        ('dividendIntervalPeriod', dtype('float64')),
        ('guaranteedEarningRate', dtype('float64')),
        ('date', dtype('<M8[ns]')),
        ('netAsset', dtype('int64')),
        ('estimatedEarningRate', dtype('float64')),
        ('investedUnits', dtype('int64')),
        ('articlesOfAssociationLink', dtype('O')),
        ('prosoectusLink', dtype('O')),
        ('websiteAddress', dtype('O')),
        ('manager', 'string[python]'),
        ('managerSeoRegisterNo', 'Int64'),
        ('auditor', 'string[python]'),
        ('custodian', 'string[python]'),
        ('guarantor', 'string[python]'),
        ('beta', dtype('float64')),
        ('alpha', dtype('float64')),
        ('isCompleted', dtype('bool')),
        ('fundWatch', dtype('O')),
    ]
    assert len(df) > 286


@patch_session('dependencygraph.json')
async def test_dependency_graph_data():
    df = await dependency_graph_data()
    assert [*df.dtypes.items()] == [
        ('regNo', dtype('int64')),
        ('name', 'string[python]'),
        ('fundType', dtype('int64')),
        ('fundSize', dtype('int64')),
        ('dailyEfficiency', dtype('float64')),
        ('weeklyEfficiency', dtype('float64')),
        ('monthlyEfficiency', dtype('float64')),
        ('quarterlyEfficiency', dtype('float64')),
        ('sixMonthEfficiency', dtype('float64')),
        ('annualEfficiency', dtype('float64')),
        ('efficiency', dtype('float64')),
        ('cancelNav', dtype('float64')),
        ('issueNav', dtype('float64')),
        ('date', dtype('<M8[ns]')),
        ('netAsset', dtype('int64')),
        ('manager', dtype('O')),
        ('guarantorId', dtype('float64')),
        ('guarantor', 'string[python]'),
        ('guarantorCode', 'string[python]'),
        ('rankOf12Month', dtype('int64')),
        ('rankOf36Month', dtype('int64')),
        ('rankOf60Month', dtype('int64')),
        ('rankLastUpdate', dtype('<M8[ns]')),
        (
            'typeOfInvest',
            CategoricalDtype(
                categories=['IssuanceAndCancellation', 'Negotiable'], ordered=False
            ),
        ),
        ('initiationDate', dtype('<M8[ns]')),
        ('beta', dtype('float64')),
        ('alpha', dtype('float64')),
    ]
    assert len(df) > 286


@patch_session('fundtopunits.json')
async def test_top_units():
    df = await fund.top_units()
    assert [*df.dtypes.items()] == [
        ('name', dtype('O')), ('percentage', dtype('float64'))]
    assert df['percentage'].sum() == 100


@patch_session('alpha_beta.json')
async def test_alpha_beta():
    df = await fund.alpha_beta(all_=False)
    assert [*df.dtypes.items()] == [('beta', dtype('float64')), ('alpha', dtype('float64'))]
    assert df.index.name == 'date'
    assert df.index.dtype == dtype('<M8[ns]')
