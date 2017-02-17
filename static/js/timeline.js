// window.onload = main;




var timelineTemplate = function(timeline) {
    var t = `
            <div class="timeline-cell">
                <div class="timeline-avatar">
                    <a><img src="${ timeline.avatar }"></a>
                </div>
                <div class="timeline-username-content">
                    <a href="#" data-id="${ timeline.user_id }">${ timeline.username }</a>
                    <time>${ timeline.created_time }</time>
                    <br>
                    <span class="span-timeline">${ timeline.content }</span>
                </div>
                <div class="timeline-operation">
                    <a class="timeline-delete" data-id="${ timeline.id }">删除</a>
                    <a class="timeline-edit" data-id="${ timeline.id }">编辑</a>
                </div>
            </div>
    `
    return t
}

$(document).ready(function(){
    //添加timeline
    $('.timeline-add-button').on('click', function(){
        var uid = $('.user-id').val()
        var content = $('.timeline-content').val()
        timeline = {
            'user_id': uid,
            'content': content,
        }
        console.log('timeline', timeline)
        var request = {
            url: '/api/timeline/add',
            type: 'post',
            data: timeline,
            success: function() {
                console.log('发布成功', arguments)
                var response = arguments[0]
                var timeline = JSON.parse(response)
                $('.timelines').append(timelineTemplate(timeline))
            },
            error: function() {
                alert('发布内容不能为空')
            }
        }
        $.ajax(request)
    })

    //绑定删除timeline按钮事件
    $('.timelines').on('click', '.timeline-delete', function(){
        var timelineId = $(this).data('id')
        var timelineCell = $(this).closest('.timeline-cell')
        var request = {
            url: '/api/timeline/delete/' + timelineId,
            type: 'get',
            data: {},
            success: function(){
                $(timelineCell).slideUp()
            },
            error: function() {
                alert('删除失败')
            }
        }
        $.ajax(request)
    })

    //编辑timeline
    $('.timelines').on('click', '.timeline-edit', function(){
        var timelineId = $(this).data('id')
        console.log('timelineId', timelineId)
        var timelineCell = $(this).closest('.timeline-cell')
        var spanTimeline = timelineCell.find('.span-timeline')
        var oldContent = spanTimeline.text()
        console.log('oldContent', oldContent)
        var timelineInput = $("<span><input class='timeline-input' type='text' value='" + oldContent  + "' /></span>")
        spanTimeline.html(timelineInput)
        var oldOperation = timelineCell.find('.timeline-operation')
        var newOperation = $("<a class='timeline-update' data-id='" + timelineId +"'>更新</a>")
        oldOperation.html(newOperation)
        $('.timelines').on('click', '.timeline-update', function(){
            var timelineId = $(this).data('id')
            var timelineCell = $(this).closest('.timeline-cell')
            var newContent = timelineCell.find('.timeline-input').val()
            var spanTimeline = timelineCell.find('.span-timeline')
            var oldOperation = timelineCell.find('.timeline-operation')
            var newOperation = $("<a class='timeline-delete' data-id='" + timelineId +"'>删除</a>   <a class='timeline-edit' data-id='" + timelineId +"'>编辑</a>")
            var timeline = {
                'content': newContent,
            }
            console.log('newContent', timeline)
            var request = {
                url: '/api/timeline/edit/' + timelineId,
                type: 'post',
                data: timeline,
                success: function(){
                   spanTimeline.text(newContent)
                   oldOperation.html(newOperation)
                },
                error: function(){
                    alert('更新失败')
                }
            }
            $.ajax(request)
        })
    })

})