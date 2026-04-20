using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("用法: minimax-docx \"标题\" \"内容\" 输出.docx");
            return;
        }

        string title = args[0];
        string content = args[1];
        string outputPath = args.Length > 2 ? args[2] : "output.docx";

        using (WordprocessingDocument doc = WordprocessingDocument.Create(outputPath, WordprocessingDocumentType.Document))
        {
            MainDocumentPart mainPart = doc.AddMainDocumentPart();
            mainPart.Document = new Document();
            Body body = new Body();

            // 添加标题
            Paragraph titlePara = new Paragraph();
            Run titleRun = new Run();
            titleRun.Append(new Text(title));
            titleRun.RunProperties = new RunProperties(
                new Bold(),
                new FontSize { Val = "48" },
                new Color { Val = "1A4D44" }
            );
            titlePara.Append(titleRun);
            titlePara.ParagraphProperties = new ParagraphProperties(
                new Justification { Val = JustificationValues.Center }
            );
            body.Append(titlePara);

            // 添加空行
            body.Append(new Paragraph());

            // 添加内容
            string[] lines = content.Split('\n');
            foreach (string line in lines)
            {
                Paragraph para = new Paragraph();
                Run run = new Run();
                run.Append(new Text(line));
                run.RunProperties = new RunProperties(
                    new FontSize { Val = "24" }
                );
                para.Append(run);
                body.Append(para);
            }

            mainPart.Document.Append(body);
            mainPart.Document.Save();
        }

        Console.WriteLine($"✅ Word文档已创建: {outputPath}");
    }
}
