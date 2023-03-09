import sentry_sdk
import redis

sentry_sdk.init(debug=True, traces_sample_rate=1.0)

def main():
    client = redis.Redis()

    with sentry_sdk.start_transaction(name="hello world"):
        # bad code:
        with sentry_sdk.start_span(op="function.call", description="bad code"):
            for i in range(100):
                client.set(f"foo:{i}", 1)

            for i in range(100):
                client.set(f"bar-{i}", 1)

        # good code:
        
        with sentry_sdk.start_span(op="function.call", description="good code"):
            with client.pipeline(transaction=False) as pipeline:
                for i in range(100):
                    pipeline.set(f"foo:{i}", 1)

                for i in range(100):
                    pipeline.set(f"bar-{i}", 1)

                pipeline.execute()


if __name__ == '__main__':
    main()
