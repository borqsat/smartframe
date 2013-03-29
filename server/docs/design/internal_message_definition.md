This document defines the internal pub/sub message format among different services/modules.

## Message format

    [message-channel] [message-content]

-   message-channel: The channel name of the message. Only the modules/processes subscribed to the channel can get the message.
-   message-content: The message content that was published to the channel. Each message channel should define its own message format.

### User

-   User information updated

        user:[uid]:info:changed [user_info]

    user_info is a json str contains the user information of [uid].

-   Joined groups updated

        user:[uid]:groups:changed [group_list]

    group_list is a json array contains all group ids that the user has joined. When user joins/leaves a group,
    the message will be publiashed.

### Group

-   Group info changed

        group:[gid]:info:changed [group_info]

    group_info is a json str contains the group information of [gid].

-   Group members changed(add/remove/user_info_updated)

        group:[gid]:member:changed [uid_list]

    uid_list is a json array contains all uids in the group.

-   Test session summary gets updated

        group:[gid]:session:changed [sid]

    Any changes of test sessions in the group should publish the message.

### Test Session

-   The test case status gets updated

        session:[sid]:testcase [tid]

    The test case status of [tid] in session [sid] gets updated.

-   Test screen changed

        session:[sid]:screen [timestamp]

    The device screen of the test session gets updated.
