
 The producer publishes a message to RabbitMQ. RabbitMQ routes it to a queue, which holds it until a consumer receives and acknowledges it.

 No consumer was taking orders, so the two published orders accumulated in the queue. Ready increased from 0 to 2.

 A delivered order moved from Ready to Unacknowledged while the worker processed it. After acknowledgement, it disappeared from both counts. In the two-order run, Management showed 1 Ready and 1 Unacknowledged during processing, then 0 for both when finished.

 It tells the client that the request was accepted for asynchronous work; it does not mean processing has completed or guarantee that it will succeed. It is not an exactly-once guarantee.
 Awaiting RabbitMQ network I/O lets the event loop run other requests and tasks instead of blocking the server thread while waiting.

 RabbitMQ may deliver up to two unacknowledged messages to that consumer. This worker awaits each order in a sequential loop, so it does not process two orders at the same time; an additional message can be waiting while the first is processed.

 Management shows two Consumers when both workers are connected. Unacknowledged can reach 2 when each worker holds one message, then falls as they acknowledge messages.

 RabbitMQ requeues an unacknowledged message after the consumer connection closes. It can be delivered again, including when a worker completed a side effect but stopped before its acknowledgement reached RabbitMQ.
 
 The loop can run other ready coroutines while the current coroutine waits. When the network operation completes, it schedules that coroutine to resume.
