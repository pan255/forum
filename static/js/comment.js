// window.onload = main;

var commentTemplate = function(comment) {
    var t = `
            <div class="bbs-content-middle-cell">
                <div class="bbs-content-middle-cell-avatar">
                    <a><img src="${ comment.avatar }"</a>
                </div>
                <div class="bbs-content-middle-cell-comments">
                    <div class="bbs-content-middle-cell-username">
                        <a href="#">${ comment.username }</a>
                        <span>${ comment.created_time }</span>
                    </div>
                    <div class="bbs-content-middle-cell-content">
                        ${ comment.content }
                    </div>
                </div>
            </div>
    `
    return t
}

$(document).ready(function(){
    //添加回复
    $('.comment-add').on('click', function(){
        var uid = $('.user-id').val()
        var tid = $('.topic-id').val()
        var content = $('.comment-content').val()
        comment = {
            'user_id': uid,
            'topic_id': tid,
            'content': content,
        }
        console.log('comment', comment)
        var request = {
            url: '/api/comment/add',
            type: 'post',
            data: comment,
            success: function() {
                console.log('回复成功', arguments)
                var response = arguments[0]
                var comment = JSON.parse(response)
                $('.comment-container').append(commentTemplate(comment))
                alert('回复成功')
            },
            error: function() {
                alert('回复失败, 请登录后回复')
            }
        }
        $.ajax(request)
    })




})