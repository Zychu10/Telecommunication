using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Win32;
using System.IO;

namespace Zadania_1_MK_SB
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        int[,] matrixH = new int[8, 16]
            { {1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0},
        {1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0},
        { 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0},
        { 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0},
        { 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0},
        { 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0},
        { 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0},
        { 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1}};

        static int[,] matrixToIntRow(int[,] matrix)
        {

            int[,] newMatrix = new int[matrix.GetLength(0), matrix.GetLength(1) / 8];
            int liczba1 = 0;
            int liczba2 = 0;
            for (int i = 0; i < matrix.GetLength(0); i++)
            {
                liczba1 = 0;
                liczba2 = 0;
                for (int j = 0; j < matrix.GetLength(1); j++)
                {
                    if (matrix[i, j] == 1 && j < 8)
                    {
                        liczba1 |= 1 << (7 - j);
                    }
                    else if (matrix[i, j] == 1 && j >= 8)
                    {
                        liczba2 |= 1 << (15 - j);
                    }
                }
                newMatrix[i, 0] = liczba1;
                newMatrix[i, 1] = liczba2;
            }
            return newMatrix;
        }

        static int[] matrixToIntColumn(int[,] matrixH)
        {

            int[] newMatrix = new int[matrixH.GetLength(1)];
            int liczba1 = 0;
            for (int i = 0; i < matrixH.GetLength(1); i++)
            {
                liczba1 = 0;

                for (int j = 0; j < matrixH.GetLength(0); j++)
                {
                    if (matrixH[j, i] == 1)
                    {
                        liczba1 |= 1 << (7 - j);
                    }
                }
                newMatrix[i] = liczba1;
            }
            return newMatrix;
        }

        static int[] iloczynZnakuIwiersza(int znak, int[,] matrixRow)
        {
            int count = 0;
            int[] suma = new int[matrixRow.GetLength(0)];
            for (int i = 0; i < suma.GetLength(0); i++)
            {
                count = 0;
                suma[i] = znak & matrixRow[i, 0];
                while (suma[i] > 0)
                {
                    count = count + (suma[i] & 1);
                    suma[i] = suma[i] >> 1;
                }
                suma[i] = count % 2;
            }
            return suma;
        }

        static int kodowanie(char litera, int[,] matrixH)
        {
            int[,] matrixRow = matrixToIntRow(matrixH);
            int[] suma = iloczynZnakuIwiersza(litera, matrixRow);
            int zakodowane = (short)(litera << 8);
            for (int i = 0; i < suma.Length; i++)
            {
                if (suma[i] == 1)
                {
                    zakodowane |= 1 << (7 - i);
                }
            }
            return zakodowane;
        }

        static int[] matrixRowNumber(int[,] matrixH)
        {
            int[,] doubleMatrixRow = matrixToIntRow(matrixH);
            int[] matrixRow = new int[matrixH.GetLength(0)];
            int liczba = 0;

            for (int i = 0; i < matrixRow.GetLength(0); i++)
            {
                liczba = 0;
                liczba = doubleMatrixRow[i, 0];
                liczba = liczba << (8);
                liczba |= doubleMatrixRow[i, 1];
                matrixRow[i] = liczba;
            }
            return matrixRow;
        }

        static int[] matrixModSumaBitow(int[] andOpMatrix)
        {
            int count = 0;

            for (int i = 0; i < andOpMatrix.GetLength(0); i++)
            {
                count = 0;
                while (andOpMatrix[i] > 0)
                {
                    count = count + (andOpMatrix[i] & 1);
                    andOpMatrix[i] = andOpMatrix[i] >> 1;
                }
                andOpMatrix[i] = count % 2;
            }
            return andOpMatrix;
        }

        static int dekodowanie(int zakodowane, int[,] matrixH)
        {
            int[] matrixRow = matrixRowNumber(matrixH);

            int[] andOpMatrix = new int[matrixH.GetLength(0)];

            for (int i = 0; i < andOpMatrix.GetLength(0); i++)
            {
                andOpMatrix[i] = zakodowane & matrixRow[i];
            }
            int[] modSumaBitow = matrixModSumaBitow(andOpMatrix);

            Boolean blad = false;
            int znak = 0;
            for (int i = 0; i < modSumaBitow.GetLength(0); i++)
            {
                if (modSumaBitow[i] != 0)
                    blad = true;
            }

            if (!blad)
            {
                znak = (zakodowane >> 8);
                return znak;
            }
            else
            {
                int wartoscMacierzy = 0;
                int pozycja1 = -1;
                int pozycja2 = -1;
                int[] matrixColumn = matrixToIntColumn(matrixH);

                for (int i = 0; i < modSumaBitow.GetLength(0); i++)
                {
                    if (modSumaBitow[i] == 1)
                    {
                        wartoscMacierzy |= 1 << (7 - i);
                    }
                }

                for (int i = 0; i < matrixColumn.GetLength(0); i++)
                {
                    if (wartoscMacierzy == matrixColumn[i])
                    {
                        pozycja1 = matrixColumn.GetLength(0) - i - 1;
                        zakodowane ^= 1 << pozycja1;
                        znak = (zakodowane >> 8);
                        return znak;
                    }
                }
                int porownanie = 0;
                for (int i = 0; i < matrixColumn.GetLength(0); i++)
                {
                    for (int j = 0; j < matrixColumn.GetLength(0); j++)
                    {
                        porownanie = (matrixColumn[i] ^ matrixColumn[j]);
                        if (porownanie == wartoscMacierzy)
                        {
                            pozycja1 = matrixColumn.GetLength(0) - i - 1;
                            pozycja2 = matrixColumn.GetLength(0) - j - 1;
                            zakodowane ^= 1 << pozycja1;
                            zakodowane ^= 1 << pozycja2;
                            znak = (zakodowane >> 8);
                            return znak;
                        }
                    }
                }
            }
            return -1;
        }
           public static string StringToBinary(string data)
            {
                StringBuilder sb = new StringBuilder();

                foreach (char c in data)
                {
                    sb.Append(Convert.ToString(c, 2).PadLeft(8, '0'));

                }
                return sb.ToString();
            }

        public static string ToBinary(char x)
        {
            char[] buff = new char[16];

            for (int i = 15; i >= 0; i--)
            {
                int mask = 1 << i;
                buff[15 - i] = (x & mask) != 0 ? '1' : '0';
            }

            return new string(buff);
        }

        
        private void Code(object sender, RoutedEventArgs e)
        {
            TextBox2.Clear();
            string binary;
            String text = TextBox1.Text;
            for(int i = 0; i < text.Length; i++)
            {
                char value = (char)kodowanie(text[i], matrixH);
                TextBox2.AppendText(ToBinary(value));
            }
        }

        private void deCode(object sender, RoutedEventArgs e)
        {
            TextBox1.Clear();
            String text = TextBox2.Text;
            char liczba;

            StringBuilder sb = new StringBuilder();

            int[] buff = new int[TextBox2.Text.Length / 16];
            
            for (var i = 0; i < TextBox2.Text.Length / 16; i++)
                buff[i] = Convert.ToInt32(TextBox2.Text.Substring(i*16, 16), 2);

            for (int i = 0; i < buff.Length; i++)
            {
                char value = (char)dekodowanie(buff[i], matrixH);
                TextBox1.AppendText(value.ToString());
            }
           
        }
        private void Zapisz1_Click(object sender, RoutedEventArgs e)
        {
            var button = (Button)sender;

            if (button != null)
            {
                SaveFileDialog tt = new SaveFileDialog();
                tt.RestoreDirectory = true;

                if (button.Name == "Zapisz1")
                {
                    tt.DefaultExt = "txt";
                    tt.Filter = "txt files (*.txt)|*.txt";
                    if (tt.ShowDialog() == true)
                    {
                        Stream fileStream = tt.OpenFile();
                        StreamWriter sw = new StreamWriter(fileStream);

                        sw.Write(TextBox1.Text);

                        sw.Close();
                        fileStream.Close();
                    }
                }
                if (button.Name == "Zapisz2")
                {
                    tt.DefaultExt = "txt";
                    tt.Filter = "txt files (*.txt)|*.txt";
                    if (tt.ShowDialog() == true)
                    {
                        Stream fileStream = tt.OpenFile();
                        StreamWriter sw = new StreamWriter(fileStream);

                        byte[] buff = new byte[TextBox2.Text.Length / 8];
                        for (var i = 0; i < TextBox2.Text.Length / 8; i++)
                        {
                            buff[i] = Convert.ToByte(TextBox2.Text.Substring(i * 8, 8), 2);
                            sw.Write((char)buff[i]);
                        }                     
                        sw.Close();
                        fileStream.Close();
                    }
                }         
            }
        }
        private void Odczytaj1_Click(object sender, RoutedEventArgs e)
        {
            var button = (Button)sender;

            if (button != null)
            {
                OpenFileDialog openFile = new OpenFileDialog();

                string line = "";

                if (button.Name == "Odczytaj1")
                {
                    if (openFile.ShowDialog() == true)
                    {
                        openFile.Filter = "txt files (*.txt)|*.txt";
                        TextBox1.Text = "";
                        StreamReader sr = new StreamReader(openFile.FileName);
                        while (line != null)
                        {
                            line = sr.ReadLine();
                            if (line != null)
                            {
                                TextBox1.Text += line;
                            }
                        }
                        sr.Close();
                    }
                }
                if (button.Name == "Odczytaj2")
                {
                    TextBox2.Clear();
                    if (openFile.ShowDialog() == true)
                    {
                        openFile.Filter = "txt files (*.txt)|*.txt";
                        TextBox1.Text = "";
                        StreamReader sr = new StreamReader(openFile.FileName);
                        while (line != null)
                        {
                            line = sr.ReadLine();
                            if (line != null)
                            {
                                TextBox2.Text += line;
                            }
                        }
                        sr.Close();                   
                        TextBox2.Text = StringToBinary(TextBox2.Text);
                    }
                }
            }
        }
    }
}
