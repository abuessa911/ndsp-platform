from app.execution.execution_learning import ExecutionLearning


class ExecutionOptimizer:

    def __init__(self):
        self.learner = ExecutionLearning()

    ########################################
    # 🧠 Generate Suggestions
    ########################################
    def suggest(self):

        stats = self.learner.analyze()

        if stats.get("status") != "ok":
            return {"status": "no_data"}

        suggestions = {}

        ########################################
        # ⚡ Optimize Delay
        ########################################
        avg_slippage = stats["avg_slippage"]

        if avg_slippage > 0.002:
            suggestions["delay"] = "increase_delay"  # زيادة التأخير
        elif avg_slippage < 0.001:
            suggestions["delay"] = "reduce_delay"  # تقليل التأخير
        else:
            suggestions["delay"] = "keep"

        ########################################
        # ⚡ Optimize Chunks
        ########################################
        avg_chunks = stats["avg_chunks"]

        if avg_chunks < 2:
            suggestions["chunks"] = "increase_chunks"  # زيادة التقسيم
        elif avg_chunks > 5:
            suggestions["chunks"] = "reduce_chunks"  # تقليل التقسيم
        else:
            suggestions["chunks"] = "keep"

        return {
            "status": "ok",
            "stats": stats,
            "suggestions": suggestions
        }
