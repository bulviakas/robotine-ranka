import threading
from ui.error_popup import ErrorPopup

def run_sequence(app, executor, sequence, lang_manager):
    def worker():
        result = executor.execute(sequence)

        def handle():
            if result.status == "hard_error":
                ErrorPopup(
                    app,
                    lang_manager.get("popup_error_hard_body", reason=result.hard_error_reason),
                    level="hard"
                )

            elif result.status == "incomplete":
                ErrorPopup(
                    app,
                    lang_manager.get(
                        "error_incomplete_body",
                        tasks="\n".join(f"- {t.capitalize()} station not visited"
                                        for t in result.missing_tasks)
                    ),
                    level="incomplete"
                )

            elif result.status == "soft_error":
                ErrorPopup(
                    app,
                    lang_manager.get("error_soft_body"),
                    level="soft"
                )
            elif result.status == "passed":
                ErrorPopup(
                    app, 
                    lang_manager.get("passed_body"),
                    level="passed"
                )

        app.root.after(0, handle)

    threading.Thread(target=worker, daemon=True).start()