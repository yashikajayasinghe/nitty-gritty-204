# Sales Team App

> Reference: 
> 1. https://learn.microsoft.com/en-us/training/modules/implement-message-workflows-with-service-bus/5-exercise-write-code-that-uses-service-bus-queues
> 2. https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
> 3. https://learn.microsoft.com/en-us/training/modules/implement-message-workflows-with-service-bus/7-exercise-write-code-that-uses-service-bus-topics
> 4. https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-topics-subscriptions

### *Service Bus Queue*

#### Run Python

```
python send_and_receive_msg_with_sb_queue.py
```

#### Output:

```
Message sent
Message received: $10,000 order for bicycle parts from retailer Adventure Works.
```

### *Service Bus Topic*

#### Run Python
```
python send_and_receive_msg_with_sb_topic.py
```

#### Output:
```
Sent a single message
Received: Didn't know you were using mushroom out of cans. I don't like that pizza.
```