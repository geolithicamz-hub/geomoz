#!/usr/bin/env python3
"""
Executor de Todos os Testes GeoMoz
Executa todos os testes em sequência e gera relatório completo
"""

import subprocess
import sys
import os
from datetime import datetime

def run_test(test_file, description):
    """
    Executa um teste específico e retorna o resultado
    """
    print(f"\n{'='*60}")
    print(f"EXECUTANDO: {description}")
    print(f"Ficheiro: {test_file}")
    print(f"{'='*60}")

    try:
        # Adicionar PYTHONPATH para encontrar geomoz
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.dirname(os.getcwd())

        result = subprocess.run([sys.executable, test_file],
                              capture_output=True, text=True, timeout=300,
                              env=env)

        if result.returncode == 0:
            print(f"Status: SUCESSO")
            return True, result.stdout
        else:
            print(f"Status: ERRO")
            print(f"Erro: {result.stderr}")
            return False, result.stderr

    except subprocess.TimeoutExpired:
        print(f"Status: TIMEOUT (5 minutos)")
        return False, "Teste excedeu tempo limite"
    except Exception as e:
        print(f"Status: ERRO - {e}")
        return False, str(e)

def main():
    """
    Função principal que executa todos os testes
    """
    print("=== EXECUTOR COMPLETO DE TESTES GEOMOZ ===")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Diretório: {os.getcwd()}")

    # Lista de testes em ordem de importância
    tests = [
        {
            'file': 'test_mozambique_complete.py',
            'description': 'Teste Completo - Mapas de Moçambique',
            'critical': True
        },
        {
            'file': 'crs_auto_example.py',
            'description': 'CRS Automático - Backend',
            'critical': True
        },
        {
            'file': 'check_cross_zone.py',
            'description': 'Verificação de Cruzamento de Zonas UTM',
            'critical': True
        },
        {
            'file': 'test_cross_zone_robust.py',
            'description': 'Teste Robusto de Cruzamento de Zonas',
            'critical': True
        },
        {
            'file': 'utm_zones_demo.py',
            'description': 'Demonstração de Zonas UTM Corrigidas',
            'critical': False
        },
        {
            'file': 'final_demo_simple.py',
            'description': 'Demonstração Final - Simplicidade',
            'critical': False
        },
        {
            'file': 'test_geomoz.py',
            'description': 'Teste Básico da Biblioteca',
            'critical': False
        }
    ]

    # Executar todos os testes
    results = []
    critical_passed = 0
    critical_total = 0

    for test in tests:
        success, output = run_test(test['file'], test['description'])

        results.append({
            'file': test['file'],
            'description': test['description'],
            'success': success,
            'output': output,
            'critical': test['critical']
        })

        if test['critical']:
            critical_total += 1
            if success:
                critical_passed += 1

    # Gerar relatório final
    print(f"\n{'='*60}")
    print("RELATÓRIO FINAL DE TESTES")
    print(f"{'='*60}")

    print(f"\nResumo Geral:")
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - passed_tests

    print(f"Total de testes: {total_tests}")
    print(f"Testes passados: {passed_tests}")
    print(f"Testes falhados: {failed_tests}")
    print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")

    print(f"\nTestes Críticos:")
    print(f"Testes críticos passados: {critical_passed}/{critical_total}")

    if critical_passed == critical_total:
        print("Status: TODOS OS TESTES CRÍTICOS PASSARAM! ")
    else:
        print("Status: ALGUNS TESTES CRÍTICOS FALHARAM! ")

    print(f"\nDetalhes dos Testes:")
    for result in results:
        status = "PASSOU" if result['success'] else "FALHOU"
        critical = " [CRÍTICO]" if result['critical'] else ""
        print(f"  {result['file']:25s} | {status:8s}{critical} | {result['description']}")

    # Salvar relatório completo
    report_content = f"""
RELATÓRIO COMPLETO DE TESTES GEOMOZ
Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESUMO GERAL:
- Total de testes: {total_tests}
- Testes passados: {passed_tests}
- Testes falhados: {failed_tests}
- Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%

TESTES CRÍTICOS:
- Testes críticos passados: {critical_passed}/{critical_total}
- Status: {'TODOS OS TESTES CRÍTICOS PASSARAM!' if critical_passed == critical_total else 'ALGUNS TESTES CRÍTICOS FALHARAM!'}

DETALHES:
"""

    for result in results:
        report_content += f"\n{result['file']} - {result['description']}"
        report_content += f"\nStatus: {'PASSOU' if result['success'] else 'FALHOU'}"
        if result['critical']:
            report_content += " [CRÍTICO]"
        report_content += f"\nSaída:\n{result['output']}\n"

    # Salvar relatório
    with open('relatorio_completo.txt', 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\nRelatório completo salvo: relatorio_completo.txt")

    # Verificar ficheiros gerados
    print(f"\nFicheiros PNG gerados:")
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]
    print(f"Total de ficheiros PNG: {len(png_files)}")

    if png_files:
        print("Lista de ficheiros:")
        for png in sorted(png_files):
            size = os.path.getsize(png)
            print(f"  {png:30s} | {size:8d} bytes")

    print(f"\n{'='*60}")
    if critical_passed == critical_total:
        print("CONCLUSÃO: Todos os testes críticos passaram!")
        print("O GeoMoz está funcionando corretamente!")
    else:
        print("CONCLUSÃO: Alguns testes críticos falharam!")
        print("Verifique os erros e corrija antes de usar o GeoMoz.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
