import quote_responder
import help_responder
import pr_responder

crontable = []
outputs = []
# channel = "C4G7HHCUW"  # TEST
channel = "C2JJFADEY"  # Pegasus team

pegasus_commands = ['pr', 'prs', 'help', 'quote']
pegasus_user_id = 'U4ERC6A3A'


def call_pegasus_response(command):
    if command == 'pr' or command == 'prs':
        message = pr_responder.main()

    if command == 'help':
        message = help_responder.main()

    if command == 'quote':
        message = quote_responder.main()

    return message

def process_message(data):
    """
    This method watches the channel data for  "@pegasus" and calls the matching pegasus
    response command if one exists.
    """

    if 'subtype' in data:
        if data['subtype'] == 'message_changed':
            original_message_channel = data['channel']
            data = data['message']
            data['channel'] = original_message_channel

    if data['user'] != pegasus_user_id:
        if data['channel'] == channel and pegasus_user_id in data['text']:

            # Strip out ; or : characters because Sam can't get it right
            stripped_text = data['text'].translate({ord(i):None for i in ';:'})
            end_position_of_pegasus_id = stripped_text.index(">") + 1
            # Add spaces after pegasus user id so it can't crash if one isn't put there
            stripped_text_with_spaces = stripped_text[:end_position_of_pegasus_id] + ' ' + stripped_text[end_position_of_pegasus_id:]

            message_from_user = stripped_text_with_spaces.split()

            pegasus_position = message_from_user.index("<@{}>".format(pegasus_user_id))

            if len(message_from_user) - 1 > pegasus_position:
                user_command = message_from_user[pegasus_position + 1].lower()

                if user_command in pegasus_commands:
                    message = call_pegasus_response(user_command)
                else:
                    message = ("Sorry, I don't recognise that command.\n"
                               "You can type *@pegasus help* for a list of available commands.")

            else:
                message = ("Please provide commands in the format *@pegasus <command>*\n"
                           "You can type *@pegasus help* for a list of avilable commands.")

            outputs.append([data['channel'], message, data['user']])
