## EndPoints List :ledger:

        End point           Description           TYPE                          Expects

1.  `admin/` => `Admin DashBoard ` `Generic View` `Super User Creds `
2.  `auth/generate_otp/`=> `Generate OTP for a phone number`. `API/POST`. `{phone_number: '', country: <country_id>}`
3.  `auth/validate_phone/` => `Validate Phone before continue reg` `API/POST`. `{phone_number: '', otp: ''}`
4.  ` auth/register/` => `Register the user `. `API/POST`. `{phone_number: '', first_name: '', username: "", "email":  "","constituency_id": <id>, "password": "", "last_name": "", dob: "". foreign_user: true/false, country: <country Id>}`
5.  `auth/sign_in/` => `Sign in with password` `API/POST` `{phone_number: '', password: ''}`
6.  `auth/generate_login_otp/` => `Generate otp for OTP login` `API/POST` `{phone_number: ''}`
7.  `auth/otp_login` => `Login with provided OTP`. `API/POST`. `{phone_number: '', otp: ''}`
8.  `auth/states/` => `API/GET`, `Get all States list`, `{}`
9.  `auth/districts/<state_id>` => `API/GET`, `Get all districts list for that state`, `{}`
10. `auth/constituencies/<district_id>` => `API/GET`, ` Get all constituencies for that district`, `{}`
11. `auth/forgot_password_otp` => `API/POST` , `Send otp for forgot password number`, `{"phone_number": <phone_number>}`
12. `auth/reset_password` => `API/POST`, `Validates otp and re-sets password for user`, `{"phone_number": <phone_number>, "otp": <otp>, "password": <password>}`
13. `auth/countries/` => `API/GET`, `Get all countries list `, {}
14. `auth/check_username` => `API/POST`, `Check if user name is already taken`, `{"username": "<username>"}`

                              FRIENDS (auth required)


15. `api/friends/create/` => `create friend request add `, `API/POST`, `{"recipient_id": whome_to_add_id, "message": "message"}`
16. `api/friends/requests_list/`=> `list of all friend requests`, `API/GET`, `{}`
17. `api/friends/list/` => `All friends list`, `API/GET`, `{}`
18. `api/friends/accept_request/<id>/` => ` API/GET`, `Accept a request with request ID`, `{}`
19. `api/friends/reject_request/<id>/` => `API/GET`, `Reject a request wurh request id`, `{}`
20. `api/friends/sent_request_list/` => `API/GET`, `Get all sent friend request list (which are not accepted yet)`, `{}`
21. `api/friends/requests_count/` => `API/GET`, `Count of all the friend request received`, `{} `
22. `api/friends/rejected_list/` => `API/GET`, `All rejected list`, `{}`
23. `api/friends/unfriend/` => `API/POST`, `Unfriend a friend`, `{"recipient_id": whome_to_remove_id}`
24. `api/friends/check_friends/` => `API/POST` , `check if two users are friends`, `{"recipient_id": other_user_id}`
25. `api/friends/unrejected_requests_list/` => `API/GET` , `Get all un rejected requests list `, `{}`

                                  NewsFeed/Posts (auth required)

26. `api/user_post_create/` => `API/POST formData`, `create a new user post file type 1 or 2. 1 for Image and 2 for Video the request is represented in json but need to use formData  ` , `{"description": "", "category": <id>, "gps_data"<nm>: "", attachments: [{"attachment": "", "file_type": 1/2},...], "tagged_user_ids": [<user_ids>] }` [example request](https://github.com/charithreddyv/r2a_backend/blob/master/examples/create_post.png)
27. `api/post/<id>/` => `API/GET` => `Get a single post data`, `{}`
28. `api/user_post/<id>/` => `API/PUT` => `Update  a specific fieds `, `{} follow same as api/user_post_create send only which needs to be updates send attachments as a empty [] if nothing needed to be added also applies for above post request pass tagged_user_ids list of ids if passed empty  or [] will remove all old tagged users` [example request](https://github.com/charithreddyv/r2a_backend/blob/master/examples/update_post.png)
29. `api/user_post/<id>/` => `API/DELETE`, `delete a user post `,`{}`
30. `api/delete_users_attachment/<id>/` => `API/DELETE`, `delete a attachment `, `{} `
31. `api/user_category_posts/<cateory>/?page=1` => `API/GET`, `for my social and medical posts Get users posts based on category 1 for political and 2 for medical this is a pagination api replace ?page=2 to get next page data you will get next page number in each response without ?page will get you first page details send param status = (1/2) to get all clarified posts and unclarified posts respectively`, `{}`
32. `api/post_comments/<post_id>/` => `API/GET` , ` returns all the comments for that specific post you will get my_comment boolean in this route to know if thus comment belongs to you or not`, `{}`
33. `api/create_comment/<post_id>` => `API/POST`, `Create a new comment for a post `, `{"message": <message string>}`
34. `api/comment_update_delete/<comment_id>` => `API/DELETE`, `Delete a specific comment (comment can be delete by the user who has created it only) to know who created this comment you will get my_comment boolean inside post_comments route`, `{}`
35. `api/comment_update_delete` => `API/PUT`, `update a specific comment (Follow same format as above )`, `{"message": ""}`
36. `api/generate_like_dislike/<post-id>` => `API/GET`, `to create or remove a like for that post by current user`, `{}`
37. `api/my_recent_posts/` => `API/GET`, `Get all my recent posts `, `{}`
38. `api/upload_attachment` => `API/POST` , `add a new attachment for a post (optional as we already have udate posts api )`, `{"attachment": <"file">, "file_type": 1/2, "post_id": <post_id> }`
39. `api/my_constituency_posts/` => `API/GET` , `Users constituency posts ` , `{}`
    All the above apis for posts are user specific
40. `api/user_recent_posts/<user_id>/` => `API/GET` , ` Get recent posts of a particular user`, `{}`
41. `api/posts/?page=1` => `API/GET`, `Get all posts this will be replaced  filter in future for pagination increment page=<number> you will get next page url in the response it self if you have next page content, add constituency=<conc_id>  or  district=<district_id>  or state=<state_id> as paramas ex: /api/posts/?page=2&state=1  sent status=(1/2) to get all clarified or not clarified posts`, `{}`

42. `api/category_posts/<category>/?page=1` => `API/GET`, `Get all posts based on category 1 for political and 2 for social and  add constituency=<conc_id>  or  district=<district_id>  or state=<state_id> for filtering as paramas ex:api/category_posts/<category>/?page=2&state=1`, `{}`
43. `api/upload_firebase/` => `API/POST`, `Uplaod data to firebase storage this takes form data of file with key as "file"`, `{file: <file >}`

                User List api

44. `api/user_list/?search=charith` => `API/GET`, `Get list of all users (pagination API) search="name" only if you want to search else it will return whole list of users  ` , `{}`
45. `api/user/<id>/` => `API/GET`, `Get user data/profile for a  particular user`, `{}`
46. `api/myprofile/` => `API/GET`, `Get Current user data`, `{}`
47. `api/myprofile/` => `API/PUT`, `update Current user data`, `{"dob": "", "last_name": "" etc..} expect phone no, email user allowed to change every other data`

                       Newly Added Apis

48. `api/toggle_post_clarified/<post_id>` => `API/GET`. `Toggle a post from unsloved to solved and vice versa `, `{}`
49. `api/my_district_posts/` => `API/GET` , `Get all my district posts for medial rep`, `{}`
50. `api/friends/delete_request/<request id>` => `API/DELETE` , `To delete a friend request (avoid using reject request api )`, `{}`
51. `auth/change_password/` => `API/PUT`, `Update password for a user`, `{"old_password": "",  "new_password": ""}`
    _Use the same generate apis to resend as well for now i have not implemented any limit it is on TODO list_

                    Modified Apis

52. `/api/category_posts/ will now accept a new param status (1/2) to filter all claried or not clarified posts `
53. `/api/posts/ will now accept a new param status (1/2) to filter all claried or not clarified posts  and also search param to search on description`

                Chats

54. `api/chats/group/`=> `API/POST` , `To create new group`, ``{"name": "<Mandatory>", "description": <nm>, "recepient_ids": [{"id": <some id>}]]}   recepient_ids: [] empty array can be passed`

55. `api/chats/group/<id>` => `API/PUT` , `Can update all The above values `

56. `api/chats/group/<id>` => `API/GET` , `Get a particular group details `

57. `api/chats/group/<id>` => `API/DELETE`, `To delete a particulat group`

58. `api/chats/my_groups` => `APi/GET`, `Get all the groups of current user `

59. `api/chats/group_users/<group_id>` => `Api/GET`, `Get all the users in that group` -> <pg>

60. `api/chats/group_messages/<group_id>` => `API/GET`, `Get Messages for a group` -> <pg>

61. `api/chats/message` => `API/PUT` => `Edit a message`, `{"message": "new message"}`

62. `api/chats/message` => `API/PUT` => `Delete a message `

    SUPPORT

63. `api/support/my_admin_tickets/` => `API/GET`, `Get all requests created by user ` -> <pg>
64. `api/support/create_ticket/` => `API/POST`, `Create a request `, `{titile: "", description: ""}`
65. `api/support/delete_admin_ticket/<id>/` => `API/DELETE`, `DELETE a request `, ` `
66. ` api/support/get_admin_ticket/<id>/` => `API/GET` , `GET a ticket by ID`

          Polls

67. `polls/list/` => `API/GEt` , `Gets list of all the polls pagination Api`, `{}`, -> <pg>
68. `polls/vote/<pollId>/`, `API/POST`, `Generate vote or remove ex: lets say a user has voted for (will get in the list api for which the user have already voted) "Yes" or id "1" and he clicks on "1" again the previous vote will be taken off else if his first vote was "1" and clicks on "2"/ "No" his vote for "1" will be removed and will be added ro "2" `, `{"choice_id": ""} `
69. `polls/commnent/<pollId>/` , `API/POST`, `create comment for a post `, `{"message": <comment Text>}`
70. `polls/comments/<pollId>/`, `API/GET`, `get list of comments on poll paginated api `, `{}` -> <pg>
71. `polls/delete_comment/<commentId>/` , `API/DELETE`, `Delete a comment user can only delete his own comment api also restricts it ` , `{}`
    Stories
72. `api/stories/my_stories/` => `API/GET` , `returns list o users having stories (the users whome logged in user is following and also logged in user )`, `{}`
73. `api/stories/delete/<story_id>/` => `ApI/DELETE`, `Delete users story by specific id `, `{}`
74. `api/stories/create/` => `API/POST FormData`, `To create a story the mandatory options are 'media_type' should have one of 4 options 1 -> image, 2-> video, 3 -> text , 4 -> other if media_type is 1 or 2 file is mandatory if its 3 text is mandatory`, ` request for media type (image/video) story {"media_type": 1/2, "file": ....jpg} for text type {"media_type": 3, "text": <some text here >}`
75. `api/stories/user/<user_id>/` => `API/GET`, `get all srories of a following user by id`, `{}`
76. `update_seen_by/<story_id>/` => `API/GET`, `Adds current user to seen by for a story `, `{}`
    Follow(s)
77. `api/followers/create/` => `API/POST`, `Follow other user `, `{"recipient_id": <other user id>}`
78. `api/followers/followers_list/` => `API/GET`, `Get all users current user is following paginated Api`, `{}` -> <pg>
79. `api/followers/following_list/` => `API/GEt`, `Get all users that are following current user PaginatedApi`, `{}` -> <pg>
80. `api/followers/unfollow/` => `API/POST`, `unfollow a following user `, `{"followee_id": <other user id>}`
81. `api/followers/users/followers_list/<User_id>/` , `API/GET`, `get searched users followers list `, `{}`
82. `api/followers/users/following_list/<user_id>/`, `API/GET`, `get seacrhed users following list`, `{}`
83. `api/followers/chatroom_id/<user_id>/` => `API/GET`, `get chatRoomId if already chatted else creates a new one and sends...`, `{}`
84. `api/followers/remove/` => `API/POST`, `remove a user from thats been following you `, `{"followee_id": <other user id>}`

85. `api/followers/search_chat_rooms/?search=<name>`, => `API/GET`, `{}`, `get all chatsRooms with search params `
    Tagged Posts
    For tagging a user to post apis look at `api/user_post_create/` to create and `api/user_post/<id>/` for update
86. `api/tagged_posts/<user_id>`, `API/GET`, `Get all posts where use is tagged in `, `{}` -> <pg>
87. `api/my_tagged_posts/`, `API/GET`, `Get all posts where current user is tagged in `, `{}` -> <pg>


    Notification
    apis for user activity notifications shown in app for someone following a user and some one tagged him in a post

93. `api/notifications/list/`, `API/GET`, `Get all user notifications `, `{}`
94. `api/notifications/count/`, `API/GET`, `Get count of unread/unseen notifications`, `{}`
95. `api/notifications/mark_all_seen/`, `API/GET`, ``marks all unread notifications as read`, `{}```


    Save Post

96. `api/save_post/<int:post id>/`, `API/GET`, `Save a post or removed from saved post if already saved`, `{}`
97. `api/saved_posts/`, `API/GET`, `returns list of all saved posts by user`, `{}` -> <pg>

Events

98. `api/events/new/`, `API/POST formData`, `create a new event`, `{"title": "", "description"<optional>: "","longitude": "", "latitude": "", "banner"<optional>: "File", "start": "YYYY-MM-DD HH:MM:SS", "end": "YYYY-MM-DD HH:MM:SS", "event_type" 1(public), 2(private): 1/2, "city": ""}`

99. `api/events/my_events/`, `API/GET`, `send list events created by logged in user `, `{}` -> <pg>

100.  `api/events/for_me`, `API/GET`, `send list for events for logged in user `, `{}` -> <pg>

[WebSockets ENDPOINTS](https://github.com/charithreddyv/r2a_backend/blob/master/wsENDPOINTS.md)

### `<nm>` stands for not mandatory field

### `<pg>` stands for not Pagiantion api NOTE: for some apis it is not added

### **NOTE:** Please comment any work which you did not complete and wish to complete later with a comment `#TODO`
