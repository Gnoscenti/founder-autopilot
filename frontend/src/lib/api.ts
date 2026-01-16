import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface Prompt {
  id: string
  title: string
  category: string
  prompt: string
}

export interface Task {
  id: string
  type: string
  title: string
  description: string
  status: string
  agent: string
  inputs?: Record<string, any>
  outputs?: Record<string, any>
  artifacts?: string[]
}

export interface Run {
  run_id: string
  status: string
  current_task_id?: string
  progress: number
}

export interface CreateRunRequest {
  goal: string
  constraints?: Record<string, any>
}

// API functions
export const getPrompts = async (): Promise<{ prompts: string[]; count: number }> => {
  const response = await api.get('/prompts')
  return response.data
}

export const getPrompt = async (promptId: string): Promise<Prompt> => {
  const response = await api.get(`/prompts/${promptId}`)
  return response.data
}

export const createRun = async (request: CreateRunRequest): Promise<Run> => {
  const response = await api.post('/runs', request)
  return response.data
}

export const getRun = async (runId: string): Promise<Run> => {
  const response = await api.get(`/runs/${runId}`)
  return response.data
}

export const getRunTasks = async (runId: string): Promise<{ run_id: string; tasks: Task[] }> => {
  const response = await api.get(`/runs/${runId}/tasks`)
  return response.data
}

export const executeNextTask = async (runId: string) => {
  const response = await api.post(`/runs/${runId}/execute`)
  return response.data
}

export const getTask = async (runId: string, taskId: string): Promise<Task> => {
  const response = await api.get(`/runs/${runId}/tasks/${taskId}`)
  return response.data
}

export const getPermissions = async (): Promise<Record<string, string[]>> => {
  const response = await api.get('/permissions')
  return response.data
}

export const getHealth = async () => {
  const response = await api.get('/health')
  return response.data
}
