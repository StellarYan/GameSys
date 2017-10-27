/**
 * @author horken wong <horken.wong@gmail.com>
 * @version: v1.0.0
 * https://github.com/horkenw/bootstrap-table
 * Click to edit row for bootstrap-table
 */

(function ($) {
    'use strict';

    $.extend($.fn.bootstrapTable.defaults, {
        clickEdit: false
    });

    function setDivision(node, options){
        var $option = $('<option />');
        if(options){
            $(options).each(function(i, v){
                $option.clone().text(v.idxNum + ' ' +v.name).val(v.name).appendTo(node);
            })
        }
        else{
            console.log('Please setup options first!!')
        }
    }

    function clikcToEdit(evt, tarNode){
        var txt = [], table = evt,
            submit = '<button type="button" class="btn btn-primary btn-sm editable-submit">确认</button>',
            cancel = '<button type="button" class="btn btn-default btn-sm editable-cancel">取消</button>';
        /*if (table.options.uniqueId=="Match") {
            $('#score').bootstrapTable({clickEdit: false});
        }*/
        var replaceData = function(){
            $.post("Set",{
                Type:"Upgrade",
                Table: table.options.uniqueId,
                TeamName: getValue('小队名称',table.$data.thId+1,table.options.uniqueId),
                TeamAccount: getValue('小队账号',table.$data.thId+1,table.options.uniqueId),
                Password: getValue('密码',table.$data.thId+1,table.options.uniqueId),
                ID:getValue('身份证号',table.$data.thId+1,table.options.uniqueId),
                Name:getValue('姓名',table.$data.thId+1,table.options.uniqueId),
                PhoneNum:getValue('电话',table.$data.thId+1,table.options.uniqueId),
                Gender:getValue('性别',table.$data.thId+1,table.options.uniqueId),
                PlayerID:getValue('运动员号',table.$data.thId+1,table.options.uniqueId),
                Age:getValue('年龄',table.$data.thId+1,table.options.uniqueId),
                Group:getValue('比赛年龄组',table.$data.thId+1,table.options.uniqueId),
                CultureScore:getValue('文化成绩',table.$data.thId+1,table.options.uniqueId),
                MatchID:getValue('比赛号',table.$data.thId+1,table.options.uniqueId),
                Event:getValue('项目',table.$data.thId+1,table.options.uniqueId),
                ChiefID:getValue('主裁判身份证',table.$data.thId+1,table.options.uniqueId),
                StartTime:getValue('预期开始时间',table.$data.thId+1,table.options.uniqueId),
                EndTime:getValue('预期结束时间',table.$data.thId+1,table.options.uniqueId),
                JudgeAccount:getValue('裁判账号',table.$data.thId+1,table.options.uniqueId),
				MatchType:getValue('比赛类型',table.$data.thId+1,table.options.uniqueId)
            });
            $('.table').bootstrapTable('updateRow', {
                index: table.$data.thId,
                row: {},
            });
            $('#tooling').remove();
            table.editing = true;
            $('#score').bootstrapTable({clickEdit: false});
            $(".table").bootstrapTable('refresh');
            return false;
        };

        var recoveryData = function(){
          $('.table').bootstrapTable('updateRow', {
                index: table.$data.thId,
                row: {},
            });
          $('#tooling').remove();
          table.editing = true;
          $('#score').bootstrapTable({clickEdit: false});
          return false;
        };

        if(table.editing){
            var  rootid = 0;
            table.editing = false;
            table.columns.forEach(function(column, i){
                if (!column.editable) return;
                switch(column.editable){
                    case 'input':
                        var div=$('<div class="editable-input col-md-12 col-sm-12 col-xs-12" style="position: relative;"/>');
                        txt.push(tarNode.find('td').eq(column.fieldIndex).text());
                        div.append($('<input type="text" class="form-control input-sm"/>'));
                        div.append($('<span class="clear"><i class="fa fa-times-circle-o" aria-hidden="true"></i></span>'));
                        tarNode.find('td').eq(column.fieldIndex).text('').append(div);
                        break;
                    case 'select':
                        var select=$('<select id="'+column.title+'" class="form-control input-sm">'), options = $.selectArray[column.field];
                        tarNode.find('td').eq(column.fieldIndex).text('').append(select);
                        setDivision($('#'+column.title), options);
                        break;
                    case 'textarea':
                        break;
                    default:
                        console.log(column.fieldIndex+' '+column.editable);
                }

            }, evt);
            for(var i=0, l=txt.length; i<l; i++){
                tarNode.find('input[type="text"]').eq(i).val(txt[i]);
            }
            tarNode.find('td').last().append('<div id="tooling" class="editable-buttons"/>');
            $('.clear').on('click', function(){ $(this).parent().find('input').val('');});
            $(submit).on('click', replaceData).appendTo('#tooling');
            $(cancel).on('click', recoveryData).appendTo('#tooling');
        }
    }

    function getValue(property,rowindex,tablename) {
        var tableTotal = 1;
        switch (tablename) {
            case "Score":
                tableTotal = 2;
                break;
            case "MatchJudge":
                tableTotal = 3;
                break;
            case "PlayMatch":
                tableTotal = 4;
                break;
            default:
                break;
        }
        //为当前页面表格的数量
        var colindex = $('.table').eq(tableTotal-1).find("[data-field]:contains('"+property+"')").index();
        var cells = document.getElementsByClassName('table')[tableTotal-1].rows[rowindex].cells
        
        if (colindex == -1) {
            var cellcontent = "";//当页面上不存在这个内容时
        }
        else if ($(cells[colindex]).find('input').length!=0) {
            var cellcontent = $(cells[colindex]).find('input').first().val();//当单元格为输入框时;
        }
        else if($(cells[colindex]).find('select').length!=0) {
            var cellcontent = $(cells[colindex]).find('select').first().val();//当单元格为下拉框时；
        }
        else {
            var cellcontent = cells[colindex].innerHTML//当单元格不可编辑时
        }
        //获取单元格内容，其中row为行序，col为列序
        return cellcontent;
    }

    var BootstrapTable = $.fn.bootstrapTable.Constructor,
        _initTable = BootstrapTable.prototype.initTable,
        _initBody = BootstrapTable.prototype.initBody;

    BootstrapTable.prototype.initTable = function(){
        var that = this;
        this.$data = {};
        _initTable.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.clickEdit) {
            return;
        }

    };

    BootstrapTable.prototype.initBody = function () {
        var that = this;
        _initBody.apply(this, Array.prototype.slice.apply(arguments));

        if (!this.options.clickEdit) {
            return;
        }

        var table = this.$tableBody.find('table');
        that.editing=true;

        table.on('click-row.bs.table', function (e, row, $element, field) {
            if(field ==='no') return; //|| field ==='noOld'
            this.$data.thId = $element.data().index;
            this.$data.itemid = $element.data().uniqueid;
            this.$data.divi = parseInt(row.area);
            this.$data.town=parseInt(row.town);
            clikcToEdit(this, $element);
        }.bind(this));
    };
})(jQuery);

