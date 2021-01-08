
var create_vue = function (data) {

  const app = new Vue({
    el: '#main',
    data: {
      current_page: 0,
      posts: data.posts,
      is_introduction: true,
      posts_html: ''
    },
    methods: {
      get_posts: function (posts_id) {

        this.is_introduction = false
        let data_a = get_data('/posts_content/?posts_id=' + posts_id)
        this.posts_html = data_a
      },

      click_tag: function (tag_id) {
        let data = get_data('/posts_head/?limit=30&tags=' + tag_id);
        this.posts = data.posts
      }
    }

  })
  return app
}


let data = get_data('/posts_head/?limit=30')
let app = create_vue(data)
