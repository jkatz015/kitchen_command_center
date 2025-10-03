const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function fetchFromApi<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json();
}

export type Task = {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
};

export type Event = {
  id: number;
  name: string;
  start: string;
  end: string;
  location: string;
  notes: string;
};

export function getTasks(): Promise<Task[]> {
  return fetchFromApi<Task[]>("/api/tasks/");
}

export function getEvents(): Promise<Event[]> {
  return fetchFromApi<Event[]>("/api/events/");
}

export { API_URL };
