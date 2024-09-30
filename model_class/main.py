from model_preparation.RAG_chain import build_rag_chain, run_rag_chain
from function_calling.TakeActionIntructor import TakeActionIntructor
import gradio as gr

rag_chain, off_rag = build_rag_chain()
take_action = TakeActionIntructor()
initial_message =  "Chào mừng bạn đến không gian trò chuyện của chúng ta. 🎉 \nTôi là trợ lý AI hỗ trợ về sức khoẻ tâm lý sau sinh 👩🏼‍⚕️. Để biết thêm các chức năng khác ngoài việc trò chuyện, vui lòng nhắn **'help'**. \nBạn cần tôi giúp gì không?"
responses = {
        "xin chào": "Chào bạn 👋🏼! Tôi là trợ lý AI hỗ trợ về sức khoẻ tâm lý sau sinh. Bạn cần tôi giúp gì không?",
        "bạn tên gì": "Tôi là trợ lý AI hỗ trợ về sức khoẻ tâm lý sau sinh. Rất vui khi được giúp đỡ bạn. ❤️",
        "tạm biệt": "Tạm biệt! Hẹn gặp lại bạn sau. 👋🏼"
    }


def rhyme_chat(message, history): 
    if take_action.check_extract_keyword(message)[0]:
        action = take_action.take_action(message)
        if take_action.keyword != "help":
            take_action.add_job_scheduler(action, scheduled_action, args = [action])
        chatbot.value.append((message, action.to_string()))
        return action.to_string()
    elif message.lower() in responses:
        chatbot.value.append((message, responses[message.lower()]))
        return responses[message.lower()]
    else:
        response= run_rag_chain(rag_chain, off_rag, message)
        print(response['source_documents'])
        chatbot.value.append((message, response['answer']))
        return response['answer']

def scheduled_action(action):
    chatbot.value.append((None, action.to_string(remind_now = True)))
    
chatbot = gr.Chatbot(height = "50vh",value=[(None, initial_message)])
gr.ChatInterface(rhyme_chat, 
                 chatbot=chatbot, 
                 examples=["Xin chào","Bạn tên gì", "remind", "appointment", "help"],
                 title="Postpartum Psychology Chatbot").launch()
