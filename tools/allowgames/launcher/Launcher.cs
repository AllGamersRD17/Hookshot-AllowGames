// Allow Games Save Editor launcher (AllGamersRD / Allow Games, GPL-3.0-or-later).
// Drag one or more progress.sav files onto AllowGames-SaveEditor.exe: each gets everything (ag_save_editor.py "all"),
// after a backup beside it. Uses the Hookshot Builder's own Python (..\tools\python\python.exe), else "python" on PATH.
// Compiled by the release workflow with the .NET Framework's csc (C# 5), so it needs nothing installed on Windows 10/11.
using System;
using System.Diagnostics;
using System.IO;

static class Launcher
{
    static int Run(string py, string script, string save, string cmd)
    {
        var psi = new ProcessStartInfo(py, "-I \"" + script + "\" \"" + save + "\" " + cmd);
        psi.UseShellExecute = false;
        var p = Process.Start(psi);
        p.WaitForExit();
        return p.ExitCode;
    }

    static void Pause()
    {
        Console.WriteLine();
        Console.WriteLine("Pulsa una tecla para cerrar / Press any key to close.");
        try { Console.ReadKey(true); } catch (InvalidOperationException) { }
    }

    static int Main(string[] args)
    {
        Console.Title = "Allow Games Save Editor";
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine("  ==============================================");
        Console.WriteLine("     SAVE EDITOR  -  ALLOW GAMES  (AllGamersRD)");
        Console.WriteLine("     para Hookshot - Allow Games Edition");
        Console.WriteLine("  ==============================================");
        Console.ResetColor();
        Console.WriteLine();

        string dir = AppDomain.CurrentDomain.BaseDirectory;
        string script = Path.Combine(dir, "ag_save_editor.py");
        string py = Path.GetFullPath(Path.Combine(dir, Path.Combine("..", Path.Combine("tools", Path.Combine("python", "python.exe")))));
        if (!File.Exists(py)) py = "python";

        if (!File.Exists(script))
        {
            Console.WriteLine("Falta ag_save_editor.py junto al .exe / ag_save_editor.py is missing next to the .exe.");
            Pause();
            return 1;
        }
        if (args.Length == 0)
        {
            Console.WriteLine("Cierra el juego y arrastra tu progress.sav encima de este .exe.");
            Console.WriteLine("Close the game and drag your progress.sav onto this .exe.");
            Console.WriteLine();
            Console.WriteLine("  <juego / game>\\user\\save\\<cuenta / account>\\slot_NN\\progress.sav");
            Console.WriteLine();
            Console.WriteLine("Siempre se guarda una copia antes (progress.sav.bak-<fecha>).");
            Console.WriteLine("A backup is always written first (progress.sav.bak-<time>).");
            Pause();
            return 1;
        }

        int rc = 0;
        foreach (string save in args)
        {
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("> " + save);
            Console.ResetColor();
            if (!File.Exists(save)) { Console.WriteLine("  no existe / not found"); rc = 1; continue; }
            try
            {
                int r = Run(py, script, save, "all");
                if (r == 0) Run(py, script, save, "show");
                Console.ForegroundColor = r == 0 ? ConsoleColor.Green : ConsoleColor.Red;
                Console.WriteLine(r == 0 ? "  LISTO / DONE: abre el juego y carga la partida." : "  ERROR (la copia de seguridad sigue ahi / the backup is still there)");
                Console.ResetColor();
                if (r != 0) rc = r;
            }
            catch (System.ComponentModel.Win32Exception)
            {
                Console.WriteLine("  No se encontro Python / Python not found (" + py + ").");
                rc = 1;
            }
            Console.WriteLine();
        }
        Pause();
        return rc;
    }
}
