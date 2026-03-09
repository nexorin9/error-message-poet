#!/usr/bin/env node
/**
 * Error Message Poet - JavaScript 示例
 * 将系统错误消息转化为诗歌
 */

const { collectErrorsFromError } = require('../error_collector.js');
const { PoetryGenerator } = require('../poetry_generator.js');
const { evaluatePoetry, generateQualityReport } = require('../poetry_quality.js');

// 示例 1: 转换单个错误消息
function exampleSingleConversion() {
    console.log('='.repeat(60));
    console.log('示例 1: 转换单个错误消息');
    console.log('='.repeat(60));

    // 模拟一个 JavaScript 错误
    try {
        const result = 1 / 0;
    } catch (error) {
        const errorObj = collectErrorsFromError(error);

        console.log(`\n原始错误消息:\n${errorObj.message}\n`);

        // 使用默认配置生成诗歌
        const generator = new PoetryGenerator();
        const poem = generator.generate(errorObj);

        console.log(`生成的诗歌:\n${poem}\n`);

        // 评估诗歌质量
        const quality = evaluatePoetry(poem, errorObj.message);
        console.log('诗歌质量评估:');
        console.log(`  综合得分: ${quality.score}/100`);
        console.log(`  流畅度: ${quality.metrics.fluency}/100`);
        console.log(`  诗意: ${quality.metrics.poeticness}/100`);
        console.log(`  准确性: ${quality.metrics.accuracy}/100`);
        console.log(`  连贯性: ${quality.metrics.coherence}/100`);
        console.log(`\n详细反馈:\n${quality.feedback}`);
    }
}

// 示例 2: 批量转换错误消息
function exampleBatchConversion() {
    console.log('\n' + '='.repeat(60));
    console.log('示例 2: 批量转换错误消息');
    console.log('='.repeat(60));

    // 模拟多个错误
    const errors = [
        {
            type: 'TypeError',
            message: 'Cannot read property of undefined',
            language: 'javascript'
        },
        {
            type: 'ReferenceError',
            message: 'x is not defined',
            language: 'javascript'
        },
        {
            type: 'RangeError',
            message: 'Maximum call stack size exceeded',
            language: 'javascript'
        }
    ];

    const generator = new PoetryGenerator();

    console.log(`\n共 ${errors.length} 个错误:\n`);

    errors.forEach((error, index) => {
        console.log(`[${index + 1}] ${error.type}: ${error.message}`);
        const poem = generator.generate(error);
        console.log(`    → ${poem}\n`);
    });
}

// 示例 3: 使用自定义模板
function exampleWithTemplates() {
    console.log('\n' + '='.repeat(60));
    console.log('示例 3: 使用自定义模板');
    console.log('='.repeat(60));

    const error = {
        type: 'TimeoutError',
        message: 'request timeout after 30 seconds',
        language: 'javascript'
    };

    const generator = new PoetryGenerator();

    // 使用现代诗模板
    console.log('\n使用现代诗模板:');
    const poem = generator.generate(error, 'modern');
    console.log(poem);

    // 使用古体诗模板
    console.log('\n使用古体诗模板:');
    const poem2 = generator.generate(error, 'classical');
    console.log(poem2);

    // 使用自由诗模板
    console.log('\n使用自由诗模板:');
    const poem3 = generator.generate(error, 'free');
    console.log(poem3);
}

// 示例 4: 生成质量报告
function exampleQualityReport() {
    console.log('\n' + '='.repeat(60));
    console.log('示例 4: 生成质量报告');
    console.log('='.repeat(60));

    const error = {
        type: 'DatabaseError',
        message: 'database connection failed',
        language: 'javascript'
    };

    const generator = new PoetryGenerator();
    const poem = generator.generate(error);

    console.log(`\n原始错误: ${error.message}`);
    console.log(`\n生成的诗歌:\n${poem}\n`);

    // 生成详细质量报告
    const report = generateQualityReport(poem, error.message);
    console.log(report);
}

// 示例 5: 错误消息分析
function exampleErrorAnalysis() {
    console.log('\n' + '='.repeat(60));
    console.log('示例 5: 错误消息分析');
    console.log('='.repeat(60));

    const { analyzeErrors, generateErrorReport } = require('../error_analyzer.js');

    const errors = [
        {
            type: 'TypeError',
            message: 'Cannot read property of undefined',
            language: 'javascript'
        },
        {
            type: 'ReferenceError',
            message: 'x is not defined',
            language: 'javascript'
        },
        {
            type: 'RangeError',
            message: 'Maximum call stack size exceeded',
            language: 'javascript'
        }
    ];

    // 分析错误
    const analysis = analyzeErrors(errors);

    // 生成报告
    const report = generateErrorReport(errors);
    console.log(report);
}

// 主函数
function main() {
    console.log('\nError Message Poet - JavaScript 示例\n');

    // 检查是否提供了示例编号
    if (process.argv.length > 2) {
        const exampleNum = parseInt(process.argv[2]);
        if (exampleNum === 1) {
            exampleSingleConversion();
        } else if (exampleNum === 2) {
            exampleBatchConversion();
        } else if (exampleNum === 3) {
            exampleWithTemplates();
        } else if (exampleNum === 4) {
            exampleQualityReport();
        } else if (exampleNum === 5) {
            exampleErrorAnalysis();
        } else {
            console.log(`未知示例编号: ${exampleNum}`);
            console.log('可用示例: 1-5');
        }
    } else {
        // 运行所有示例
        exampleSingleConversion();
        exampleBatchConversion();
        exampleWithTemplates();
        exampleQualityReport();
        exampleErrorAnalysis();
    }

    console.log('\n' + '='.repeat(60));
    console.log('示例运行完成');
    console.log('='.repeat(60));
}

// 运行主函数
main();