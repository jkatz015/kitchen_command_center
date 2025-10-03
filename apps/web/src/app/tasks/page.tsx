import { getTasks } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function TasksPage() {
  const tasks = await getTasks();

  return (
    <main className="mx-auto flex w-full max-w-4xl flex-col gap-6 p-6">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">Tasks</h1>
        <p className="mt-2 text-sm text-slate-600">
          Stay on top of your kitchen operations by reviewing the latest tasks
          pulled from the command center backend.
        </p>
      </header>

      <section className="rounded-lg border bg-background p-4 shadow-sm">
        {tasks.length === 0 ? (
          <p className="text-sm text-slate-600">
            No tasks yet. Add one via the Django admin or API to see it here.
          </p>
        ) : (
          <ul className="space-y-3">
            {tasks.map((task) => (
              <li
                key={task.id}
                className="flex items-center justify-between rounded-md border p-3"
              >
                <div>
                  <p className="font-medium">{task.title}</p>
                  <p className="text-xs text-slate-500">
                    Created {new Date(task.created_at).toLocaleString()}
                  </p>
                </div>
                <span
                  className={
                    task.completed
                      ? "rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-700"
                      : "rounded-full bg-amber-100 px-3 py-1 text-sm font-semibold text-amber-700"
                  }
                >
                  {task.completed ? "Completed" : "Pending"}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
