$(function () {//主函数逻辑，在页面渲染完毕后执行

    refresh_op();//页面启动，触发刷新函数
    setInterval(function () {
        refresh_op();
    },5000);
    $('#search_btn').click(function () {//搜索按钮添加监听事件
        refresh_op()
    });

    $('#add_business').click(function () {//为添加业务按钮监听事件，当被点击时获取业务数据并弹框
        loading_open();
        $.ajax({
            url: site_url + 'get_busines_by_user/',
            type: 'get',
            success: function (data) {
                loading_close();
                if (data['result']) {
                    model_open(data)
                } else {
                    alert('获取数据失败')
                }
            }
        })
    })
});


//刷新函数，获取数据并触发绘制表格函数
var refresh_op = function () {
    filter_key = {'InnerIP': $('#ip_search').val()};
    $.ajax({
        url: site_url + 'get_host/',
        type: 'get',
        data: filter_key,
        success: function (data) {
            if (data.result) {
                draw_table(data);
            } else {
                time_dialog('获取数据失败，请联系管理员！')
            }
        }
    })
};


//添加业务的弹框函数
var model_open = function (data) {
    //生成下拉框html代码
    var html_r = '<select id="sel_t" class="form-control">';
    for (i in data['data']) {
        html_r = html_r + '<option value=' + data['data'][i]['app_id'] + '>' + data['data'][i]['bussiness'] + '</option>'
    }
    html_r = html_r + '</select>';
    var d = dialog({//生成弹窗
        width: 260,
        title: '请选择业务',
        content: '<div>' + html_r + '</div>',
        okValue: '确定',
        ok: function () {
            //点击保存后，触发上传数据的函数
            up_data()
        },
        cancelValue: '取消',
        cancel: function () {
        }
    });
    d.showModal();
};


//上传数据
var up_data = function () {
    loading_open();
    //点取确定：把用户选择的业务的id获取下来，传递给后台，后台接口通过业务id获取主机信息并把信息存入数据库
    $.ajax({
        url: site_url + 'add_business/',
        type: 'post',
        data: {app_info: $('#sel_t').val()},
        success: function (data) {
            loading_close()
            if (data.result) {
                time_dialog('添加成功');
                refresh_op()//添加成功后，刷新页面数据
            } else {
                error_dialog('添加失败，请联系管理员')
            }
        }
    })
};


//绘制表格的函数，传入数据源
var draw_table = function (data) {
    //获取窗口高度，nav导航栏高度，查询栏高度，计算表格高度（container有一个内边距30px，底部留一些空隙，所以最后减掉60）
    var window_h = $(window).height();
    var nav_h = $('.navbar').height();
    var field_h = $('fieldset').height();
    var table_height = window_h - nav_h - field_h - 60 - 94;

    $('#table_container').kendoGrid({
        height: table_height,
        pageable: {
            pageSize: 10, //如果要显示分页，必须设置pageSize
            buttonCount: 3,
        },
        dataSource: {
            data: data['data']//数据源[{}]
        },
        columns: [
            {
                field: 'bussiness',
                title: '业务名称'
            },
            {
                field: 'ip',
                title: 'IP'
            },{
                field: 'cpu_monitor',
                title: 'CPU使用率(%)'
            },
            {
                field: 'creator',
                title: '创建者'
            },
            {
                template: "<div style='text-align: center'><button class='btn btn-sm btn-danger' onclick='del(#: id #)'>删除</button>" +
                "<button class='btn btn-sm btn-info' onclick='detail(#: id #)'>查看</button></  div>",// 绑定数据字段age
                title: "操作" // 设置列头显示的title
            }
        ],
    });
};

var del = function (id) {
    var d = dialog({
        width: 260,
        title: '提示',
        content: '确定删除么？',
        cancel: true,
        ok: function () {
            $.ajax({
                url: site_url + 'del_server/',
                type: 'post',
                data: {'id': id},
                success: function (data) {
                    loading_close();
                    if (data.result) {
                        time_dialog('删除成功');
                        refresh_op()//添加成功后，刷新页面数据
                    } else {
                        error_dialog('删除失败，请联系管理员')
                    }
                }
            })
        }
    });
    d.show();
};
var detail = function (id) {
    loading_open();
    $.ajax({
        url: site_url + 'get_host_by_id/',
        type: 'get',
        data: {'id': id},
        success: function (data) {
            loading_close();
            if (data.result) {
                var d = dialog({
                    width: 460,
                    height:350,
                    title: '信息',
                    content: '<div>IP：'+data['data']['ip']+'</div>' +
                    '<div>配置信息：<textarea style="height: 300px;width: 100%" id="config_text"></textarea></div>',
                    cancel: false,
                    ok: function () {
                    }
                });
                d.show();
                $('#config_text').val(data['data']['config_dsc'])
            } else {
                time_dialog('获取数据失败，请联系管理员！')
            }
        }
    })
};

//提示框
var info_dialog = function (text) {
    var d = dialog({
        width: 260,
        title: '提示',
        content: text,
        cancel: false,
        ok: function () {
        }
    });
    d.show();
};
//错误提示框
var error_dialog = function (text) {
    var d = dialog({
        width: 260,
        title: '错误',
        content: text,
        cancel: false,
        ok: function () {
        }
    });
    d.show();
};

//倒计时提示框
var time_dialog = function (text, time_s) {
    //time_s 为倒计时事件，设置默认值为3000，如果不赋值则为3000
    time_s = 3000 || time_s;
    var d = dialog({
        width: 260,
        title: '错误',
        content: text,
        cancel: false,
        ok: function () {
        }
    });
    d.show();
    setTimeout(function () {
        d.close().remove();
    }, time_s);
};

// 请求中提示框打开
var loading_open = function () {
    $('.bg_loading').css('display', 'block')
};
// 请求中提示框关闭
var loading_close = function () {
    $('.bg_loading').css('display', 'none')
};


