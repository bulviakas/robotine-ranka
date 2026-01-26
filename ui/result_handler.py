import threading
from ui.error_popup import ErrorPopup

def run_sequence(app, executor, sequence, lang_manager):
    def worker():
        result = executor.execute(sequence)

        def handle():
            if result.status == "hard_error":
                ErrorPopup(
                    app,
                    # TODO fix the reason output
                    lang_manager.get("popup_error_hard_body", reason=result.hard_error_reason),
                    level="hard"
                )

            elif result.status == "incomplete":
                tasks_text = "\n".join(
                    f"- {lang_manager.get(f'incomplete_task_{task}')}"
                    for task in result.missing_tasks
)
                ErrorPopup(
                    app,
                    lang_manager.get(
                        "popup_error_incomplete_body",
                        tasks=tasks_text
                    ),
                    level="incomplete"
                )

            elif result.status == "soft_error":
                ErrorPopup(
                    app,
                    # TODO display the list of missing tasks
                    lang_manager.get("popup_error_soft_body"),
                    level="soft"
                )
            elif result.status == "passed":
                ErrorPopup(
                    app, 
                    lang_manager.get("popup_passed_body"),
                    level="passed"
                )

        app.root.after(0, handle)

    threading.Thread(target=worker, daemon=True).start()