import threading
from ui.error_popup import ErrorPopup

def run_sequence(app, executor, sequence, lm):
    def worker():
        result = executor.execute(sequence)

        def handle():
            if result.status == "hard_error":
                ErrorPopup(
                    app,
                    lm.get("error_hard_body", reason=result.hard_error_reason),
                    level="hard"
                )

            elif result.status == "incomplete":
                ErrorPopup(
                    app,
                    lm.get(
                        "error_incomplete_body",
                        tasks=", ".join(result.missing_tasks)
                    ),
                    level="incomplete",
                    on_ok=lambda: executor.recover("Incomplete sequence")
                )

            elif result.status == "soft_error":
                ErrorPopup(
                    app,
                    lm.get("error_soft_body"),
                    level="soft"
                )
            elif result.status == "passed":
                ErrorPopup(
                    app, 
                    lm.get("passed_body"),
                    level="passed"
                )

        app.root.after(0, handle)

    threading.Thread(target=worker, daemon=True).start()