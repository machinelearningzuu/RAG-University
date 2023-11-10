css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = r'''
<div class="chat-message bot">
    <div class="avatar">
        <img src='https://scontent.fcmb2-2.fna.fbcdn.net/v/t39.30808-6/370046225_1463738167737970_78850002207142101_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=5f2048&_nc_ohc=EGbKIjApIt8AX8ISmGp&_nc_ht=scontent.fcmb2-2.fna&oh=00_AfDAzrRuumSZTroavX7z0WVbU3WOhAYmq-yiPXJhHdAcBA&oe=655073B0'>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = r'''
<div class="chat-message user">
    <div class="avatar">
        <img src='https://scontent.fcmb2-2.fna.fbcdn.net/v/t39.30808-6/369163874_1982088558843002_7945477684635534081_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=5f2048&_nc_ohc=OnV8HNYpGg8AX8dN8yl&_nc_ht=scontent.fcmb2-2.fna&oh=00_AfDKjLw5azL0s_iOStWrJ8EsETDE4haQ5yvb3VwJNsX2YQ&oe=6550A748'>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''