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
                $option.clone().text(v.idxNum + ' ' +v.name).val(v.idxNum).appendTo(node);
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
        if (table.options.uniqueId=="Match") {
            $('#score').bootstrapTable({clickEdit: false});
        }
        var replaceData = function(){
            $.post(window.location.hostname+"/GameAdmin/Set",{
                Type:"Upgrade",
                Table: table.options.uniqueId,
                TeamName: getValue('TeamName',table.$data.thId+1,table.options.uniqueId),
                TeamAccount: getValue('TeamAccount',table.$data.thId+1,table.options.uniqueId),
                Password: getValue('Password',table.$data.thId+1,table.options.uniqueId),
                ID:getValue('ID',table.$data.thId+1,table.options.uniqueId),
                Name:getValue('Name',table.$data.thId+1,table.options.uniqueId),
                PhoneNum:getValue('PhoneNum',table.$data.thId+1,table.options.uniqueId),
                Gender:getValue('Gender',table.$data.thId+1,table.options.uniqueId),
                PlayerID:getValue('PlayerID',table.$data.thId+1,table.options.uniqueId),
                Age:getValue('Age',table.$data.thId+1,table.options.uniqueId),
                Group:getValue('Group',table.$data.thId+1,table.options.uniqueId),
                CultureScore:getValue('CultureScore',table.$data.thId+1,table.options.uniqueId),
                MatchID:getValue('MatchID',table.$data.thId+1,table.options.uniqueId),
                Event:getValue('Event',table.$data.thId+1,table.options.uniqueId),
                ChiefID:getValue('ChiefID',table.$data.thId+1,table.options.uniqueId),
                StartTime:getValue('StartTime',table.$data.thId+1,table.options.uniqueId),
                EndTime:getValue('EndTime',table.$data.thId+1,table.options.uniqueId),
                JudgeAccount:getValue('JudgeAccount',table.$data.thId+1,table.options.uniqueId),
				MatchType:getValue('MatchType',table.$data.thId+1,table.options.uniqueId)
            },function () {
                $(".table").bootstrapTable('refresh');
            }); 
            $('.table').bootstrapTable('updateRow', {
                index: table.$data.thId,
                row: {},
            });
            $('#tooling').remove();
            table.editing = true;
            $('#score').bootstrapTable({clickEdit: false});
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
                        var select=$('<select id="'+column.field+'" class="form-control input-sm">'), options = $.selectArray[column.field];
                        tarNode.find('td').eq(column.fieldIndex).text('').append(select);
                        setDivision($('#'+column.field), options);
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
        var colindex = $('.table').eq(tableTotal-1).find("[data-field='"+ property +"']").index();
        var cells = document.getElementsByClassName('table')[tableTotal-1].rows[rowindex].cells
        
        if ($(cells[colindex]).find('input')) {
            var cellcontent = $(cells[colindex]).find('input').first().val();//当单元格为输入框时;
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

