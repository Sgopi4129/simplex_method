import { execFile } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import { NextResponse } from "next/server";

const run = promisify(execFile);

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const projectRoot = path.resolve(process.cwd(), "..");
    const python = process.env.PYTHON_PATH || path.join(projectRoot, ".venv", "Scripts", "python.exe");
    const runner = "import json, sys; from simplex import SimplexMethod; data=json.loads(sys.argv[1]); result=SimplexMethod(data['objective'], data['constraints'], data['limits'], data['relations'], data['sense']).solve(); print(json.dumps({'solution': result['solution'], 'maximum': result['maximum']}))";
    const { stdout } = await run(python, ["-c", runner, JSON.stringify(body)], { cwd: path.join(projectRoot, "backend") });
    return NextResponse.json(JSON.parse(stdout));
  } catch (error) {
    const message = error instanceof Error ? error.message : "The simplex calculation failed.";
    return NextResponse.json({ error: message }, { status: 400 });
  }
}