// 报名表js code

//全局变量
var A = 5;
var B = 3;

var playerCnt = 1;
var judgeCnt = 1;
var couchCnt = 1;

//设置数组存放数目信息
var array = new Array(42);

function loadFemale(check) {
    var insertText = '<div class="checkbox" style="width:1000px"><label></label><label><input type="checkbox" value="TM" name="checkbox' + check + 'Option">跳马</label><label></label><label><input type="checkbox" value="GD" name="checkbox' + check + 'Option">高低杠</label><label></label><label><input type="checkbox" value="PH" name="checkbox' + check + 'Option">平衡木</label><label></label><label><input type="checkbox" value="TC" name="checkbox' + check + 'Option">自由体操</label><label></label><label><input type="checkbox" value="BC" name="checkbox' + check + 'Option">蹦床</label><label></label></div>';
    var checktxt = 'checkbo' + check;
    document.getElementById(checktxt).innerHTML = insertText;
}
function loadMale(check) {
    var insertText = '<div class="checkbox" style="width:1000px"><label></label><label><input type="checkbox" value="DG" name="checkbox' + check + 'Option">单杠</label><label></label><label><input type="checkbox" value="SG" name="checkbox' + check + 'Option">双杠</label><label></label><label><input type="checkbox" value="DH" name="checkbox' + check + 'Option">吊环</label><label></label><label><input type="checkbox" value="TM" name="checkbox' + check + 'Option">跳马</label><label></label><label><input type="checkbox" value="TC" name="checkbox' + check + 'Option">自由体操</label><label></label><label><input type="checkbox" value="AM" name="checkbox' + check + 'Option">鞍马</label><label></label><label><input type="checkbox" value="BC" name="checkbox' + check + 'Option">蹦床</label><label></label></div>';
    var checktxt = 'checkbo' + check;
    document.getElementById(checktxt).innerHTML = insertText;
}
//设置cookies
function setCookie(c_name, value, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString());
}
function setCookies() {
    setCookie('playerCnt', playerCnt, 1);
    setCookie('judgeCnt', judgeCnt, 1);
    setCookie('couchCnt', couchCnt, 1);
}

//判断报名信息是否符合要求
function judge() {
    putmessage();
    var jud = 0;
    //判断人数是否满足要求，并设置提醒，具体为：array[0-5]<=A，array[6 - 41] <= B
    var i = 0;
    //判断年龄段性别人数
    while (i < 6) {
        if (array[i] >= A) {
            jud = 1;
            if (i == 0)
                alert("7-8年龄段男生超过人数限制");
            else if (i == 1)
                alert("7-8年龄段女生超过人数限制");
            else if (i == 2)
                alert("9-10年龄段男生超过人数限制");
            else if (i == 3)
                alert("9-10年龄段女生超过人数限制");
            else if (i == 4)
                alert("11-12年龄段男生超过人数限制");
            else
                alert("11-12年龄段女生超过人数限制");
        }
        i++;
    }
    clear(jud);
    var jage;
    var jsex;
    var jproject;
    while (i < 42) {
        //如果人数超出限制
        if (array[i] >= B) {
            jud = 2;
            //获得年龄段&性别信息
            if ((i >= 21) && (i <= 27)) {
                jage = "7-8年龄段";
                jsex = "男生";
            }
            else if (i <= 10) {
                jage = "7-8年龄段";
                jsex = "女生";
            }
            else if ((i >= 28) && (i <= 34)) {
                jage = "9-10年龄段";
                jsex = "男生";
            }
            else if ((i >= 11) && (i <= 15)) {
                jage = "9-10年龄段";
                jsex = "女生";
            }
            else if ((i >= 35) && (i <= 41)) {
                jage = "11-12年龄段";
                jsex = "男生";
            }
            else if ((i >= 16) && (i <= 20)) {
                jage = "11-12年龄段";
                jsex = "女生";
            }
            //男子项目
            if ((i == 21) || (i == 28) || (i == 35)) {
                jproject = "单杠";
            }
            else if ((i == 22) || (i == 29) || (i == 36)) {
                jproject = "双杠";
            }
            else if ((i == 23) || (i == 30) || (i == 37)) {
                jproject = "吊环";
            }
            else if ((i == 24) || (i == 31) || (i == 38)) {
                jproject = "跳马";
            }
            else if ((i == 25) || (i == 32) || (i == 39)) {
                jproject = "自由体操";
            }
            else if ((i == 26) || (i == 33) || (i == 40)) {
                jproject = "鞍马";
            }
            else if ((i == 27) || (i == 34) || (i == 41)) {
                jproject = "蹦床";
            }
                //女子项目
            else if ((i == 6) || (i == 11) || (i == 16)) {
                jproject = "跳马";
            }
            else if ((i == 7) || (i == 12) || (i == 17)) {
                jproject = "高低杠";
            }
            else if ((i == 8) || (i == 13) || (i == 18)) {
                jproject = "平衡木";
            }
            else if ((i == 9) || (i == 14) || (i == 19)) {
                jproject = "自由体操";
            }
            else if ((i == 10) || (i == 15) || (i == 20)) {
                jproject = "蹦床";
            }
            //输出信息
            alert(jage + jsex + jproject + "项目超过人数限制");
        }
        i++;
    }
    clear(jud);
}
//清除单选框和复选框信息
function clear(jud) {
    var selectvalue = null;

    if (jud == 1) {
        //获取单选框选中的值
        var radio = document.getElementsByName("sex" + playerCnt + "Option");
        for (nn = 0; nn < radio.length; nn++) {
            if (radio[nn].checked) {
                radio[nn].checked = false;
                break;
            }
        }
    }
    else if (jud == 2) {
        //获取复选框的值
        var checkbox = document.getElementsByName("checkbox" + playerCnt + "Option");
        for (k = 0; k < checkbox.length; k++) {
            if (checkbox[k].checked)
                checkbox[k].checked = false;
        }
    }
    else;
}

//添加运动员信息操作
function putmessage() {
    var j = 0;
    while (j < 42) {
        array[j] = 0;
        j++;
    }
    var i = 0;
    while (i < playerCnt) {
        i++;
        //获取年龄组信息
        var groups = document.getElementById("playergroup" + i);
        //获取下拉列表框中的值
        var index = groups.selectedIndex;

        //获取单选框选中的值
        var obj = document.getElementsByName("sex" + i + "Option");
        //获取复选框的值
        var checkbox = document.getElementsByName("checkbox" + i + "Option");

        if (index == 0)//7-8年龄组
        {
            //男生
            if (obj[0].checked) {
                array[0]++;
                for (k = 0; k < checkbox.length; k++) {
                    if (checkbox[k].checked)
                        array[k + 21]++;
                }
            }
                //女生
            else {
                array[1]++;
                for (k = 0; k < checkbox.length; k++) {
                    if (checkbox[k].checked)
                        array[k + 6]++;
                }
            }

        }
        else if (index == 1)//9-10年龄组
        {
            //男生
            if (obj[0].checked) {
                array[2]++;
                for (k = 0; k < checkbox.length; k++) {
                    if (checkbox[k].checked)
                        array[k + 28]++;
                }
            }
                //女生
            else {
                array[3]++;
                for (k = 0; k < checkbox.length; k++) {
                    if (checkbox[k].checked)
                        array[k + 11]++;
                }
            }
        }
        else//10-11年龄组
        {
            //男生
            if (obj[0].checked) {
                array[4]++;
                for (k = 0; k < checkbox.length; k++) {
                    if (checkbox[k].checked)
                        array[k + 35]++;
                }
            }
                //女生
            else {
                array[5]++;
                for (k = 0; k < checkbox.length; k++) {
                    if (checkbox[k].checked)
                        array[k + 16]++;
                }
            }
        }
    }
}
//相应的删除操作
function delmessage() {
    var i = playerCnt;
    var groups = document.getElementById("playergroup" + i);
    var index = groups.selectedIndex;
    var obj = document.getElementsByName("sex" + i + "Option");
    var checkbox = document.getElementsByName("checkbox" + i + "Option");

    if (index == 0)//7-8年龄组
    {
        //男生
        if (obj[0].checked) {
            array[0]--;
            for (k = 0; k < checkbox.length; k++) {
                if (checkbox[k].checked)
                    array[k + 21]--;
            }
        }
            //女生
        else {
            array[1]--;
            for (k = 0; k < checkbox.length; k++) {
                if (checkbox[k].checked)
                    array[k + 6]--;
            }
        }

    }
    else if (index == 1)//9-10年龄组
    {
        if (obj[0].checked) {
            array[2]--;
            for (k = 0; k < checkbox.length; k++) {
                if (checkbox[k].checked)
                    array[k + 28]--;
            }
        }
        else {
            array[3]--;
            for (k = 0; k < checkbox.length; k++) {
                if (checkbox[k].checked)
                    array[k + 11]--;
            }
        }
    }
    else//10-11年龄组
    {
        if (obj[0].checked) {
            array[4]--;
            for (k = 0; k < checkbox.length; k++) {
                if (checkbox[k].checked)
                    array[k + 35]--;
            }
        }
        else {
            array[5]--;
            for (k = 0; k < checkbox.length; k++) {
                if (checkbox[k].checked)
                    array[k + 16]--;
            }
        }
    }
}

//运动员表单插入
function insRow() {
    putmessage();
    playerCnt += 1;
    var insertText = '<hr><div class="row"><div class="col-xs-3" style="width:150px"><label for="exampleInputEmail1">姓名</label><input required type="text" class="form-control" placeholder="姓名" name="playerName' + playerCnt + '"></div><div class="col-xs-3" style="width:150px"><label for="exampleInputEmail1">年龄</label><input required type="text" class="form-control" placeholder="年龄" name="playerAge' + playerCnt + '"></div><div class="col-xs-3" style="width:150px"><label for="exampleInputEmail1">组别</label><select class="form-control" id="playergroup' + playerCnt + '"><option value ="7-8岁" name="group' + playerCnt + 'Option1">7-8岁</option><option value ="9-10岁" name="group' + playerCnt + 'Option2">9-10岁</option><option value="11-12岁" name="group' + playerCnt + 'Option1">11-12岁</option></select></div><div class="col-xs-3" style="width:100px"><label for="exampleInputEmail1">文化成绩</label><input required type="text" class="form-control" placeholder="不填" disabled="disabled"></div><div class="col-xs-3"><label for="exampleInputEmail1">身份证</label><input  required type="text" class="form-control" placeholder="身份证" name="playerID' + playerCnt + '"></div><div class="col-xs-3" style="width:150px"><label for="exampleInputEmail1">性别</label><div class="form-group"><div class="radio"><label><input type="radio" name="sex' + playerCnt + 'Option" id="optionsRadios1" value="option' + playerCnt + '" onClick="loadMale(' + playerCnt + ')">男</label><label><input type="radio" name="sex' + playerCnt + 'Option" id="optionsRadios2" value="option' + playerCnt + '" onClick="loadFemale(' + playerCnt + ')">女</label></div></div></div><div class="col-xs-3"><label for="exampleInputEmail1">比赛项目（多选）</label><div  class="form-group" id="checkbo' + playerCnt + '" name="checkbo' + playerCnt + '"><div class="checkbox" style="width:1000px"><label></label><label><input type="checkbox" value="DG" name="checkbox' + playerCnt + 'Option">单杠</label><label></label><label><input type="checkbox" value="SG" name="checkbox' + playerCnt + 'Option">双杠</label><label></label><label><input type="checkbox" value="DH" name="checkbox' + playerCnt + 'Option">吊环</label><label></label><label><input type="checkbox" value="TM" name="checkbox' + playerCnt + 'Option">跳马</label><label></label><label><input type="checkbox" value="TC" name="checkbox' + playerCnt + 'Option">自由体操</label><label></label><label><input type="checkbox" value="AM" name="checkbox' + playerCnt + 'Option">鞍马</label><label></label><label><input type="checkbox" value="BC" name="checkbox' + playerCnt + 'Option">蹦床</label><label></label></div></div></div></div><div  id="sporter' + playerCnt + '" ></div>';
    document.getElementById("sporter" + (playerCnt - 1)).innerHTML += insertText;
    document.getElementById("delete").class = "btn btn-danger";
}
//教练员表单插入
function insRow2() {
    couchCnt += 1;
    var insertText = '<hr><div class="row"><div class="col-xs-3" style="width:150px"><label for="exampleInputEmail1">姓名</label><input type="text" class="form-control" placeholder="姓名"  name="couchName' + couchCnt + '"></div><div class="col-xs-3" style="width:150px"><label for="exampleInputEmail1">性别</label><input type="text" class="form-control" placeholder="性别" name="couchSex' + couchCnt + '"></div><div class="col-xs-4" style="width:200px"><label for="exampleInputEmail1">联系方式</label><input type="text" class="form-control" placeholder="联系方式" name="couchTel' + couchCnt + '"></div><div class="col-xs-5"><label for="exampleInputEmail1">身份证号</label><input type="text" class="form-control" placeholder="身份证号" name="couchID' + couchCnt + '"></div></div></div><div class="box-body"  id="couch' + couchCnt + '"></div>';
    document.getElementById("couch" + (couchCnt - 1)).innerHTML += insertText;
}
//裁判员表单插入
function insRow3() {
    judgeCnt += 1;
    var insertText = '<hr><div class="row"><div class="col-xs-3"><label for="exampleInputEmail1">姓名</label><input type="text" class="form-control" placeholder="姓名" name="judgeName' + judgeCnt + '"></div><div class="col-xs-4"><label for="exampleInputEmail1">联系方式</label><input type="text" class="form-control" placeholder="联系方式"  name="judgeTel' + judgeCnt + '"></div><div class="col-xs-5"><label for="exampleInputEmail1">身份证号</label><input type="text" class="form-control" placeholder="身份证号"  name="judgeID' + judgeCnt + '"></div></div></div><div class="box-body"  id="judge' + judgeCnt + '"></div>';
    document.getElementById("judge" + (judgeCnt - 1)).innerHTML += insertText;
}
//运动员表单删除
function delRow() {
    if (playerCnt > 1) {
        delmessage();
        playerCnt--;
        document.getElementById("sporter" + playerCnt).innerHTML = "";
    }
    else
        alert("必须至少一个运动员！");
}
//教练员表单删除
function delRow2() {
    if (couchCnt > 1) {
        couchCnt--;
        document.getElementById("couch" + couchCnt).innerHTML = "";
    }
    else
        alert("必须至少一个教练！");
}
//裁判员表单删除
function delRow3() {
    if (judgeCnt > 1) {
        judgeCnt--;
        document.getElementById("judge" + judgeCnt).innerHTML = "";
    }
    else
        alert("必须至少一个裁判！");
}
//警告框---拒绝用户进入查看报名信息界面
function disp_alert() {
    alert("您尚未提交报名信息！")
}
//警告框---拒绝用户进入查看赛事安排表
function disp() {
    alert("您尚未报名！")
}